#!/usr/bin/env python3
"""Build the war climax's art overlay from the reference games (read-only).

  python3 -I tools/build_war_assets.py            (run from anywhere)

Writes PNGs into  plugins/Prismfall Cutscenes/Graphics/{Characters,Animations,Pictures}/  with the prefix pfw_
and prints a credits table (docs/CREDITS.md holds the copy). Nothing from the games is executed; map and
tileset data are decoded with mapgen/rmarshal.py.
Sources: /home/claude/ref/games/{rejuvenation,reborn}  (used with the user's permission, personal project).
"""
import os, sys, json
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(HERE)
GAME_ROOT = os.path.dirname(os.path.dirname(PLUGIN))          # /home/claude/fangame
sys.path.insert(0, os.path.join(GAME_ROOT, "mapgen"))
import rmarshal
import render
import terrain
import rdraw                      # the map team's own tile painter (soft ice, cracks, drifts, banners)
import math, random
from PIL import ImageDraw

REF = "/home/claude/ref/games"
OUT = os.path.join(PLUGIN, "Graphics")
CREDITS = []


def src(game, sub, name):
    return os.path.join(REF, game, "Graphics", sub, name)


def save(img, sub, name, origin, note):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    img.save(os.path.join(OUT, sub, name + ".png"))
    CREDITS.append((sub + "/" + name + ".png", origin, note))


def copy(game, sub, name, new, note="copied unchanged"):
    save(Image.open(src(game, sub, name)).convert("RGBA"), sub, new, "%s: Graphics/%s/%s" % (game.capitalize(), sub, name), note)


def recolour(img, mapping):
    """Exact-colour remap (keeps the pixel art's palette discipline)."""
    a = np.array(img.convert("RGBA"))
    out = a.copy()
    for (r, g, b), (r2, g2, b2) in mapping.items():
        m = (a[:, :, 0] == r) & (a[:, :, 1] == g) & (a[:, :, 2] == b) & (a[:, :, 3] > 0)
        out[m, 0], out[m, 1], out[m, 2] = r2, g2, b2
    return Image.fromarray(out)


def tint(img, rgb, amount):
    """Hue-shift by blending each opaque pixel's colour towards rgb, keeping luminance steps."""
    a = np.array(img.convert("RGBA")).astype(np.float32)
    lum = (a[:, :, 0] * 0.3 + a[:, :, 1] * 0.59 + a[:, :, 2] * 0.11) / 255.0
    for i in range(3):
        target = np.clip(lum * rgb[i] * 1.35, 0, 255)
        a[:, :, i] = a[:, :, i] * (1 - amount) + target * amount
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))



def outline_dark(img):
    """Darken the darkest ~12% of opaque pixels to a near-black outline so small sprites read on pale ice."""
    a = np.array(img.convert("RGBA"))
    lum = a[:, :, 0] * 0.3 + a[:, :, 1] * 0.59 + a[:, :, 2] * 0.11
    m = (a[:, :, 3] > 0) & (lum < 70)
    a[m, 0], a[m, 1], a[m, 2] = 30, 26, 44
    return Image.fromarray(a)


def up2(img):
    return img.resize((img.width * 2, img.height * 2), Image.NEAREST)


def kyogre_side():
    """Side-on acting sheet for the beam shots (kitbash): Reborn's overworld Kyogre, right-facing row, doubled to
    the Primal sheet's size and pushed to its deeper palette. Row 0 = swim loop, row 1 = markings lit (firing)."""
    im = Image.open(src("reborn", "Characters", "pkmn_kyogre.png")).convert("RGBA")
    cw, ch = im.width // 4, im.height // 4
    sheet = Image.new("RGBA", (cw * 2 * 4, ch * 2 * 2), (0, 0, 0, 0))
    for row in range(2):
        for c in range(4):
            cell = np.array(up2(im.crop((c * cw, 2 * ch, c * cw + cw, 3 * ch)))).astype(np.int32)
            r, g, b, al = cell[:, :, 0], cell[:, :, 1], cell[:, :, 2], cell[:, :, 3]
            blue = (b > r + 30) & (al > 0)                       # body blues -> Primal's deeper navy
            red = (r > 150) & (g < 90) & (b < 90) & (al > 0)     # the markings
            out = cell.copy()
            out[blue, 0] = (r[blue] * 0.45).astype(np.int32)
            out[blue, 1] = (g[blue] * 0.62).astype(np.int32)
            out[blue, 2] = np.clip(b[blue] * 0.95 + 8, 0, 255).astype(np.int32)
            if row == 1:
                out[red, 0], out[red, 1], out[red, 2] = 255, 226, 120
            sheet.alpha_composite(Image.fromarray(out.astype(np.uint8)), (c * cw * 2, row * ch * 2))
    save(sheet, "Characters", "pfw_kyogre_side", "Reborn: Graphics/Characters/pkmn_kyogre.png",
         "kitbash: right-facing row doubled to 192x128 cells, Primal palette; row 1 = markings lit (4x2)")


def banners():
    """War banners as 1x1 sheets (the map team's banner painter, doubled twice so they stand over a rank)."""
    for name, cols in (("pfw_banner_isenmar", rdraw.TEAL), ("pfw_banner_ashkaar", [(110, 24, 30, 255), (206, 52, 44, 255), (250, 190, 80, 255)])):
        im, _ = rdraw.banner(cols)
        save(up2(up2(im)), "Characters", name, "Prismfall mapgen/rdraw.py banner()", "own art, 4x scale (64x128)")


RAMP_SEA = [(14, 30, 96), (30, 84, 200), (70, 160, 250), (160, 232, 255), (255, 255, 255)]
RAMP_FIRE = [(96, 16, 30), (212, 56, 32), (250, 140, 40), (255, 226, 120), (255, 255, 255)]


def clash_core():
    """The meeting point: Fusion Flare's rayed sun re-ramped so its left half burns blue, its right half orange and
    the middle white-hot, with Ice Burn's star laid over the centre. 4 cells of 192 (two sizes of flare, mirrored)."""
    ff = Image.open(src("rejuvenation", "Animations", "PRAS- Fusion Flare.png")).convert("RGBA")
    ib = Image.open(src("rejuvenation", "Animations", "PRAS- Ice Burn.png")).convert("RGBA")
    sun = ff.crop((2 * 192, 2 * 192, 3 * 192, 3 * 192))            # cell 12
    stars = [ib.crop((2 * 192, 0, 3 * 192, 192)), ib.crop((3 * 192, 0, 4 * 192, 192))]
    sheet = Image.new("RGBA", (192 * 4, 192), (0, 0, 0, 0))
    a = np.array(sun).astype(np.float32)
    lum = (a[:, :, 0] * 0.3 + a[:, :, 1] * 0.59 + a[:, :, 2] * 0.11) / 255.0
    op = a[:, :, 3] > 0
    lo, hi = lum[op].min(), lum[op].max()
    lum = np.clip((lum - lo) / max(hi - lo, 1e-3), 0, 1)
    yy, xx = np.mgrid[0:192, 0:192]
    rad = np.sqrt((xx - 96.0) ** 2 + (yy - 96.0) ** 2)
    for i in range(4):
        out = np.zeros((192, 192, 4), dtype=np.uint8)
        wob = np.sin((yy + i * 13) * 0.21) * 7 + np.sin((yy - i * 29) * 0.08) * 6      # ragged seam between the halves
        left = (xx + wob) < 96
        lv = np.clip(lum + (0.42 if i % 2 else 0.3) * np.clip(1 - rad / 30.0, 0, 1), 0, 1)
        idx = np.minimum((lv * 4.999).astype(int), 4)
        for k in range(5):
            m = op & (idx == k)
            for side, ramp in ((left, RAMP_SEA), (~left, RAMP_FIRE)):
                mm = m & side
                out[mm, 0], out[mm, 1], out[mm, 2], out[mm, 3] = ramp[k][0], ramp[k][1], ramp[k][2], 255
        hot = op & (rad < (20 if i % 2 else 16))
        out[hot] = [255, 255, 255, 255]
        cell = Image.fromarray(out)
        star = stars[i % 2]
        sa = np.array(star)
        dark = (sa[:, :, 3] > 0) & (sa[:, :, 0].astype(int) + sa[:, :, 1] + sa[:, :, 2] < 200)   # the star's black pip -> white
        sa[dark] = [255, 255, 255, 255]
        star = Image.fromarray(sa)
        if i >= 2: star = star.rotate(45, resample=Image.NEAREST)
        cell.alpha_composite(star)
        if i >= 2: cell = cell.transpose(Image.FLIP_TOP_BOTTOM)
        sheet.alpha_composite(cell, (i * 192, 0))
    save(sheet, "Animations", "pfw_fx_clash_core",
         "Rejuvenation: Graphics/Animations/PRAS- Fusion Flare.png + PRAS- Ice Burn.png",
         "kitbash: sun cell re-ramped blue | white-hot | orange with the ice star over it; 4x1 cells of 192")
    shards = Image.new("RGBA", (192 * 4, 192), (0, 0, 0, 0))
    for i, (cx, cy) in enumerate([(0, 0), (1, 0), (3, 1), (4, 1)]):       # ice boulder, chunk, two shards
        shards.alpha_composite(ib.crop((cx * 192, cy * 192, cx * 192 + 192, cy * 192 + 192)), (i * 192, 0))
    save(shards, "Animations", "pfw_fx_ice_chunks", "Rejuvenation: Graphics/Animations/PRAS- Ice Burn.png",
         "4x1 cells of 192: ice boulder, chunk, two shards (thrown from the clash)")


WATER = [(34, 52, 104, 255), (52, 84, 140, 255), (84, 128, 190, 255)]


def fracture():
    """The ice breaking under the clash: 4 growing frames, drawn in the map tiles' style (dark lead + lit lower lip,
    loose plates), logical 224x112 doubled to 448x224. Ellipse-squashed for the overworld's 3/4 view."""
    W2, H2 = 224, 112
    rng = random.Random(926)
    arms = []
    for k in range(9):
        ang = k * (2 * math.pi / 9) + rng.uniform(-0.25, 0.25)
        pts = [(0.0, 0.0)]
        x = y = 0.0
        L = rng.uniform(70, 104)
        d = 0.0
        while d < L:
            step = rng.uniform(5, 10)
            ang2 = ang + rng.uniform(-0.55, 0.55)
            x += math.cos(ang2) * step; y += math.sin(ang2) * step
            d += step
            pts.append((x, y))
        arms.append(pts)
        if k % 2 == 0:                                   # a branch
            j = rng.randrange(2, max(3, len(pts) - 2))
            bx, by = pts[j]; bang = ang + rng.choice((-1, 1)) * rng.uniform(0.6, 1.0)
            bp = [(bx, by)]
            for _ in range(rng.randrange(3, 6)):
                bx += math.cos(bang + rng.uniform(-0.4, 0.4)) * 7; by += math.sin(bang + rng.uniform(-0.4, 0.4)) * 7
                bp.append((bx, by))
            arms.append(bp)
    sheet = Image.new("RGBA", (W2 * 2 * 4, H2 * 2), (0, 0, 0, 0))
    for f in range(4):
        reach = (0.3, 0.55, 0.8, 1.0)[f] * 104
        im = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        tr = lambda p: (W2 / 2 + p[0], H2 / 2 + p[1] * 0.46)
        for pts in arms:
            for a, b in zip(pts, pts[1:]):
                if math.hypot(*b) > reach: break
                A, B = tr(a), tr(b)
                wide = math.hypot(*a) < reach * 0.45
                d.line([A[0], A[1] + 1, B[0], B[1] + 1], fill=rdraw.ICE[3])                    # lit lower lip
                if wide: d.line([A[0], A[1] + 2, B[0], B[1] + 2], fill=rdraw.ICE[3])
                d.line([A, B], fill=WATER[0], width=2 if wide else 1)
                if wide: d.line([A[0], A[1] - 1, B[0], B[1] - 1], fill=WATER[1])
        r0 = (5, 9, 13, 17)[f]                                                                  # the hole at the centre
        d.ellipse([W2 / 2 - r0 * 1.6, H2 / 2 - r0 * 0.7, W2 / 2 + r0 * 1.6, H2 / 2 + r0 * 0.7], fill=WATER[0], outline=rdraw.ICE[3])
        d.ellipse([W2 / 2 - r0, H2 / 2 - r0 * 0.4, W2 / 2 + r0 * 0.6, H2 / 2 + r0 * 0.2], fill=WATER[1])
        prng = random.Random(40)
        for k in range(6 + f * 4):                                                              # loose plates
            ang = prng.uniform(0, 6.28); rr = prng.uniform(0.2, 0.9) * reach
            px, py = tr((math.cos(ang) * rr, math.sin(ang) * rr))
            if rr > reach * 0.95: continue
            d.polygon([(px - 3, py), (px, py - 2), (px + 3, py - 1), (px + 2, py + 1)], fill=rdraw.SNOW[3], outline=rdraw.ICE[0])
        sheet.alpha_composite(up2(im), (f * W2 * 2, 0))
    save(sheet, "Animations", "pfw_fx_fracture", "own art (drawn by tools/build_war_assets.py in the rdraw tile style)",
         "4x1 cells of 448x224: the ice cracking outward under the clash")


def dome():
    """The dome of Bleed light: a hand-shaded glass hemisphere, 4 shimmer frames, logical 240x150 doubled to
    480x300. Semi-transparent body, hard pixel rim, ground ring, travelling glints."""
    W2, H2 = 240, 150
    PINK, MINT, VIO, WHITE = (255, 176, 232), (112, 224, 216), (136, 96, 216), (255, 255, 255)
    cx, base, rx, ry, top = 120, 118, 112, 26, 108
    sheet = Image.new("RGBA", (W2 * 2 * 4, H2 * 2), (0, 0, 0, 0))
    for f in range(4):
        a = np.zeros((H2, W2, 4), dtype=np.uint8)
        yy, xx = np.mgrid[0:H2, 0:W2]
        nx = (xx - cx) / float(rx)
        up = (base - yy) / float(top)
        dome_in = ((yy <= base) & (nx ** 2 + up ** 2 <= 1.0)) | ((yy > base) & (nx ** 2 + ((yy - base) / float(ry)) ** 2 <= 1.0))
        edge = np.sqrt(nx ** 2 + np.where(yy <= base, up, (yy - base) / float(ry)) ** 2)
        # body: violet glass, thicker (more opaque) toward the rim; 2-step banding, checker dither between bands
        band = np.where(edge > 0.9, 2, np.where(edge > 0.7, 1, 0))
        dither = ((xx + yy) % 2 == 0)
        alpha = np.select([band == 2, band == 1], [120, np.where(dither, 96, 64)], default=np.where(dither, 52, 34))
        col = np.select([band[..., None] == 2, band[..., None] == 1], [np.array(PINK), np.array(VIO)], default=np.array(MINT))
        a[dome_in, :3] = col[dome_in]
        a[dome_in, 3] = alpha[dome_in]
        rim = dome_in & (edge > 0.965)
        a[rim] = [WHITE[0], WHITE[1], WHITE[2], 235]
        rim2 = dome_in & (edge > 0.93) & ~rim
        a[rim2] = [PINK[0], PINK[1], PINK[2], 200]
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        d.arc([cx - rx, base - ry, cx + rx, base + ry], 0, 180, fill=WHITE + (235,))              # ground ring, front
        d.arc([cx - rx, base - ry, cx + rx, base + ry], 180, 360, fill=PINK + (110,))            # and far side
        for k in range(3):                                                                      # meridians drift
            ph = ((k + f / 4.0) / 3.0) * 2 - 1
            w = abs(ph) * rx
            if w < 8: continue
            box = [cx - w, base - top, cx + w, base + top]
            d.arc(box, 180, 360, fill=(MINT if k % 2 else PINK) + (120,))
        d.arc([cx - rx + 14, base - top + 10, cx + rx - 40, base + top - 40], 200, 250, fill=WHITE + (230,), width=2)   # big glint
        g = random.Random(5)
        for k in range(14):                                                                     # sparkles twinkle
            ang = g.uniform(3.3, 6.1); rr = g.uniform(0.3, 0.92)
            px, py = cx + math.cos(ang) * rr * rx, base + math.sin(ang) * rr * top
            if (k + f) % 4 == 0:
                d.line([px - 2, py, px + 2, py], fill=WHITE + (255,)); d.line([px, py - 2, px, py + 2], fill=WHITE + (255,))
            elif (k + f) % 4 == 1:
                d.point([px, py], fill=WHITE + (255,))
        sheet.alpha_composite(up2(im), (f * W2 * 2, 0))
    save(sheet, "Animations", "pfw_fx_dome", "own art (drawn by tools/build_war_assets.py)",
         "4x1 cells of 480x300: Bleed-light dome with shimmer; anchor = ground centre at (240, 236) in the cell")


# --------------------------------------------------------------------------- characters
def characters():
    copy("rejuvenation", "Characters", "pkmn_kyogre2.png", "pfw_kyogre_rise", "4x4: emerge from the water (0-5), sink (6-7), splashes (8-15)")
    copy("rejuvenation", "Characters", "pkmn_kyogre.png", "pfw_kyogre_primal", "4x4: Primal Kyogre facing the camera; row 3 = markings glow layers")
    copy("reborn", "Characters", "pkmn_kyogre.png", "pfw_kyogre", "4x4 overworld charset (row 2 faces right)")
    copy("reborn", "Characters", "pkmn_reshiram.png", "pfw_reshiram", "4x4 overworld charset (row 1 faces left, turbine lit)")
    copy("reborn", "Characters", "pkmn_reshiram1.png", "pfw_reshiram_hover", "4x4 front-facing hover / wingbeats")
    for game, name, new in [("reborn", "pkmn_walrein.png", "pfw_walrein"), ("rejuvenation", "pkmn_sealeo.png", "pfw_sealeo"),
                            ("reborn", "pkmn_beartic.png", "pfw_beartic"), ("rejuvenation", "pkmn_houndoom.png", "pfw_houndoom"),
                            ("reborn", "pkmn_camerupt.png", "pfw_camerupt"), ("reborn", "pkmn_charizard.png", "pfw_charizard"),
                            ("reborn", "pkmn_salamence.png", "pfw_salamence")]:
        copy(game, "Characters", name, new, "4x4 overworld follower sprite (army unit)")
    grunt = Image.open(src("rejuvenation", "Characters", "Grunt_1.png")).convert("RGBA")
    save(outline_dark(tint(grunt, (58, 122, 184), 0.8)), "Characters", "pfw_soldier_isenmar",
         "Rejuvenation: Graphics/Characters/Grunt_1.png", "recoloured Isenmar teal-blue (#3A7AB8 cloth), darker outline")
    save(outline_dark(tint(grunt, (214, 60, 44), 0.8)), "Characters", "pfw_soldier_ashkaar",
         "Rejuvenation: Graphics/Characters/Grunt_1.png", "recoloured Ashkaar crimson, darker outline")
    kyogre_side()
    banners()
    knight = Image.open(src("rejuvenation", "Characters", "knight.png")).convert("RGBA")
    save(tint(knight, (150, 200, 255), 0.5), "Characters", "pfw_eirik",
         "Rejuvenation: Graphics/Characters/knight.png", "recoloured pale blue (Thane Eirik stand-in)")
    save(tint(knight, (255, 110, 60), 0.55), "Characters", "pfw_hrothgar",
         "Rejuvenation: Graphics/Characters/knight.png", "recoloured red-gold (Dominar Hrothgar stand-in)")


# --------------------------------------------------------------------------- effects
BEAM_SEA = {(239, 240, 240): (96, 184, 248), (250, 219, 235): (48, 112, 224), (253, 237, 245): (160, 224, 255),
            (250, 245, 219): (232, 250, 255), (253, 250, 237): (255, 255, 255)}
BEAM_FIRE = {(239, 240, 240): (248, 136, 48), (250, 219, 235): (200, 56, 40), (253, 237, 245): (255, 184, 80),
             (250, 245, 219): (255, 236, 160), (253, 250, 237): (255, 255, 228)}


def outline(img, rgb):
    """1px dark outline around opaque pixels (beams read on bright snow)."""
    a = np.array(img.convert("RGBA"))
    op = a[:, :, 3] > 0
    grow = op.copy()
    grow[1:, :] |= op[:-1, :]; grow[:-1, :] |= op[1:, :]; grow[:, 1:] |= op[:, :-1]; grow[:, :-1] |= op[:, 1:]
    edge = grow & ~op
    a[edge] = [rgb[0], rgb[1], rgb[2], 255]
    return Image.fromarray(a)


def effects():
    beam = Image.open(src("rejuvenation", "Characters", "anim_beam.png")).convert("RGBA")
    # 4x4 cells of 96x64, each a vertical segment with its rounded head at the bottom. Turn them so the head
    # points right (+x): each cell becomes 64x96; the sheet keeps the 4x4 layout.
    cw, ch = beam.width // 4, beam.height // 4
    for name, mapping, line in (("pfw_beam_sea", BEAM_SEA, (16, 40, 120)), ("pfw_beam_fire", BEAM_FIRE, (110, 24, 40))):
        col = recolour(beam, mapping)
        sheet = Image.new("RGBA", (ch * 4, (cw // 2) * 4), (0, 0, 0, 0))
        for r in range(4):
            for c in range(4):
                cell = col.crop((c * cw, r * ch, c * cw + cw, r * ch + ch)).rotate(90, expand=True)   # head -> right
                thin = cell.resize((cell.width, cell.height // 2), Image.NEAREST)                     # half as thick
                sheet.alpha_composite(outline(thin, line), (c * ch, r * (cw // 2)))
        save(sheet, "Characters", name, "Rejuvenation: Graphics/Characters/anim_beam.png",
             "recoloured, turned 90 degrees (head points right), half thickness, 1px outline; 4x4 cells of 64x48")
    for name, new, note in [("PRAS- Explosions.png", "pfw_fx_explosions", "4x3 cells of 192: burst 0-3, flash+smoke 4-7"),
                            ("PRAS- Steam Eruption.png", "pfw_fx_steam", "5x4 cells of 192: geyser 0-4, steam 5-9, icy burst 9"),
                            ("PRAS- Origin Pulse.png", "pfw_fx_origin_pulse", "5x3 cells of 192: water orb 0-3, geyser 5-9"),
                            ("PRAS- Fusion Flare.png", "pfw_fx_fusion_flare", "5x5 cells of 192: sun 0, flame swirls, suns 11-12"),
                            ("PRAS- Light that Burns the Sky.png", "pfw_fx_sky_burn", "5x5 cells of 192: flame grow 5-9, die 10-12")]:
        copy("rejuvenation", "Animations", name, new, note)
    clash_core()
    fracture()
    dome()


# --------------------------------------------------------------------------- stage map
W, H = 64, 24
SNOW, ICE, LEAD = 2475, 2476, 144        # Kristiline Town (Frozen): snow, sea ice, KristilineWatersFrozen autotile
CLIFF = [761, 689, 690]                  # cliff faces
LEDGE = 1485                             # ledge base with snow lip


def soften_ice(img, d, lead, shore):
    """Swap Kristiline's saturated striped ice for the pale blue-white ice Frostwick (map 570) uses: rdraw.soft_ice
    on every ice cell and inside the lead autotile's ice corners, then pressure cracks, snowdrifts and floes."""
    a = np.array(img)
    ice_cells = (d[0] == ICE) & (d[1] == 0)
    ys, xs = np.where(ice_cells)
    y0, x0 = [(y, x) for y, x in zip(ys, xs) if y > shore + 1][0]
    old = {tuple(c) for c in a[y0 * 32:(y0 + 1) * 32, x0 * 32:(x0 + 1) * 32, :3].reshape(-1, 3)}     # the striped ice's colours
    soft = [np.array(up2(rdraw.soft_ice(v))) for v in range(4)]
    rng = random.Random(570)
    pick = [[rng.choice((0, 0, 0, 1, 2, 3)) for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            cell = a[y * 32:(y + 1) * 32, x * 32:(x + 1) * 32]
            if ice_cells[y, x]:
                cell[:, :, :] = soft[pick[y][x]]
            elif lead[y, x]:
                flat = cell[:, :, :3].reshape(-1, 3)
                m = np.array([tuple(c) in old for c in flat]).reshape(32, 32)
                cell[m] = soft[0][m]
    out = Image.fromarray(a)
    free = lambda x, y: 0 <= x < W and shore + 1 < y < H and ice_cells[y, x]
    used = set()
    for _ in range(26):                                   # pressure ridges: runs of crack tiles
        x, y = rng.randrange(0, W), rng.randrange(shore + 2, H)
        for k in range(rng.randrange(2, 6)):
            if free(x + k, y) and (x + k, y) not in used:
                out.alpha_composite(up2(rdraw.crack(rng.randrange(1, 9))), ((x + k) * 32, y * 32)); used.add((x + k, y))
    for _ in range(70):                                   # snowdrifts
        x, y = rng.randrange(0, W), rng.randrange(shore + 2, H)
        if free(x, y) and (x, y) not in used:
            out.alpha_composite(up2(rdraw.drift(rng.randrange(1, 7) * 2)), (x * 32, y * 32)); used.add((x, y))
    for y in range(shore + 2, H - 1):                     # floes on open water away from the edges
        for x in range(1, W - 1):
            if lead[y, x] and lead[y - 1, x] and lead[y + 1, x] and lead[y, x - 1] and lead[y, x + 1] and rng.random() < 0.22:
                if not (15 <= x <= 26 and 8 <= y <= 14):  # keep Kyogre's pool clear
                    out.alpha_composite(up2(rdraw.floe(rng.randrange(1, 9))), (x * 32, y * 32))
    return out


def stage():
    root = os.path.join(REF, "rejuvenation")
    tss = rmarshal.load_file(os.path.join(root, "Data/Tilesets.rxdata"))
    t = tss[93]
    s = lambda v: v.decode("utf-8", "replace") if isinstance(v, (bytes, bytearray)) else str(v)
    ts = {"tileset_name": s(t.tileset_name), "autotile_names": [s(a) for a in t.autotile_names],
          "priorities": [int(v) for v in t.priorities.data.flatten()]}
    town = rmarshal.load_file(os.path.join(root, "Data/Map328.rxdata")).data.data
    d = np.zeros((3, H, W), dtype=np.int64)
    d[0, :, :] = ICE
    shore = 6                              # land rows 0..shore-1, cliff face on shore-1, ledge on shore
    d[0, :shore, :] = SNOW
    rng = np.random.RandomState(7)

    def paste(sx, sy, w, h, dx, dy):
        for yy in range(h):
            for xx in range(w):
                ty, tx = dy + yy, dx + xx
                if 0 <= ty < shore - 1 and 0 <= tx < W:
                    for z in range(3):
                        v = int(town[z, sy + yy, sx + xx])
                        if z == 0:
                            d[0, ty, tx] = v if v >= 384 else SNOW
                        elif v:
                            d[z, ty, tx] = v
    for i, dx in enumerate(range(-4, W, 14)):     # forest band (trunks sit just above the cliff)
        paste(47, 3, 14, 9, dx, -4)
    paste(35, 6, 12, 9, 3, -4)                    # glass-roofed hall on Isenmar's shore
    for x in range(W):
        d[1, shore - 1, x] = CLIFF[rng.randint(0, 3)] if rng.rand() < 0.3 else CLIFF[0]
        d[2, shore - 1, x] = 0
        d[1, shore, x] = LEDGE
    # open water: Kyogre's pool and the leads between plates
    lead = np.zeros((H, W), dtype=bool)
    yy, xx = np.mgrid[0:H, 0:W]
    lead |= ((xx - 20.5) / 4.6) ** 2 + ((yy - 11.0) / 2.4) ** 2 < 1.0
    noise = terrain.vnoise if hasattr(terrain, "vnoise") else None
    for y in range(shore + 2, H):
        for x in range(W):
            n = noise(x, y, 11, 2.2) if noise else rng.rand()
            army = (y >= 13 and (x < 19 or x > 36))
            under = 17 <= x <= 36 and 9 <= y <= 14                 # the legendaries and the beam line
            if under:
                continue
            if n > (0.86 if army else 0.74):
                lead[y, x] = True
    # a black-water crack running from the clash point to the shore and out to sea
    x, y = 27.0, 9.0
    for step in range(60):
        lead[int(y), int(x)] = True
        if step % 3 == 0 and 0 <= int(x) + 1 < W:
            lead[int(y), int(x) + 1] = True
        y += 0.38
        x += float(np.sin(step * 0.55) * 0.9) + 0.15
        if y >= H - 1:
            break
    d[0][lead] = LEAD
    terrain.autotile_layer(d, 0, LEAD)

    class M: pass
    m = M()
    m.width, m.height = W, H

    class T: pass
    m.data = T(); m.data.data = d
    m.events = {}
    render.GFX = os.path.join(root, "Graphics")
    render.OUT_GFX = "/nonexistent"
    img = render.render(m, events=False, ts=ts).convert("RGBA")
    img = soften_ice(img, d, lead, shore)
    save(img.convert("RGBA"), "Pictures", "pfw_shattered_ice",
         "Rejuvenation: tileset 'Kristiline Town (Frozen)' + autotiles, tiles from Map328 (Kristiline Town); ice from Prismfall mapgen/rdraw.py",
         "composed %dx%d-tile frozen strait; sea ice repainted with the map team's pale soft ice, cracks, drifts and floes (temporary stage until map 926 exists)" % (W, H))
    json.dump({"tiles": [W, H], "shore_row": shore, "pool": [20.5, 11.0]},
              open(os.path.join(OUT, "Pictures", "pfw_shattered_ice.json"), "w"))


if __name__ == "__main__":
    characters()
    effects()
    stage()
    print("| File | Source | Changes |")
    print("|---|---|---|")
    for f, o, n in CREDITS:
        print("| `%s` | %s | %s |" % (f, o, n))
