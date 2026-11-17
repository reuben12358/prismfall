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
    save(tint(grunt, (140, 200, 255), 0.45), "Characters", "pfw_soldier_isenmar",
         "Rejuvenation: Graphics/Characters/Grunt_1.png", "recoloured icy blue (Isenmar soldier)")
    save(tint(grunt, (255, 110, 70), 0.5), "Characters", "pfw_soldier_ashkaar",
         "Rejuvenation: Graphics/Characters/Grunt_1.png", "recoloured crimson (Ashkaar soldier)")
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


# --------------------------------------------------------------------------- stage map
W, H = 64, 24
SNOW, ICE, LEAD = 2475, 2476, 144        # Kristiline Town (Frozen): snow, sea ice, KristilineWatersFrozen autotile
CLIFF = [761, 689, 690]                  # cliff faces
LEDGE = 1485                             # ledge base with snow lip


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
    img = render.render(m, events=False, ts=ts)
    save(img.convert("RGBA"), "Pictures", "pfw_shattered_ice",
         "Rejuvenation: tileset 'Kristiline Town (Frozen)' + autotiles, tiles from Map328 (Kristiline Town)",
         "composed %dx%d-tile frozen strait (temporary stage for :WAR_CLIMAX until map 926 exists)" % (W, H))
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
