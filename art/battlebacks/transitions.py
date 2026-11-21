#!/usr/bin/env python3
"""Staged field transitions: assets for the Bridge's in-room transitions (008_Bridge_Transitions.rb).

  python3 -I art/battlebacks/transitions.py          # (also run by build_backdrops.py with GLASS_DUNES)

GLASS QUENCH (FLOODED_DUNES -> GLASS_DUNES, DESERT -> GLASS_DUNES). The old swap faded the whole room to a flat mint
card for 8 frames and back (the battlers floating on nothing), then everything of the glass room popped in at once.
Now the change happens IN the room, from where the white fire hit:
  * an arrival-time map over the glass room: geodesic distance from the impact point (the foe's or the player's
    base), fast along the old flood water (it flash-heats first), slower over sand, slowest over rock; the sky is
    reached last, climbing up from the horizon as the white-fire haze;
  * that map cut into BANDS time steps: rvNN.png holds the glass room's own pixels of band NN (transparent elsewhere),
    so the runtime reveals the glass band by band over the old room;
  * hkNN.png: the heat of band NN, ground only - a white-hot rim along its leading edge and a dim amber body behind
    it, drawn additive and cooled through orange at runtime (the sky only changes under the reveal: no glare);
  * ltNN.png: a crackle of light through the new glass - the shortest heat paths from the impact to points across
    the glass (a branching network that follows the old water) plus the room's own amber cooling seams, cut into the
    same bands, flashed in order after the front;
  * steam puffs rise where the front crosses the old water (points per band in the generated Ruby);
  * impact glow and a perspective heat ring.
Everything is in HD room space (864x693, 2 HD px per art pixel), drawn by the Bridge as room layers so EBDX's camera
moves it with the room and the battlers stay on top.

Writes graphics/EBDX/Battlebacks/transitions/glass_quench/ and plugins/Prismfall EBDX Bridge/009_Bridge_Transition_Art.rb.
"""
import sys, os, json, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
from skimage.graph import MCP_Geometric
from bblib import HD, FOE, PLAYER, arr, img, noise, OUT

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RB_OUT = os.path.join(ROOT, "plugins", "Prismfall EBDX Bridge", "009_Bridge_Transition_Art.rb")
TR_DIR = os.path.join(OUT, "transitions")
BANDS = 16
RIM = 0.3                                       # leading share of a band that glows white-hot
AW, AH = HD[0] // 2, (HD[1] + 1) // 2          # art grid (2 HD px per art pixel)
WHITE_HOT = (255, 252, 236)


def _art(a):
    """HD array -> art grid (top-left HD pixel of each 2x2 block)."""
    return a[::2, ::2][:AH, :AW]


def _hd(a):
    """art grid -> HD array (nearest, cropped)."""
    return np.repeat(np.repeat(a, 2, 0), 2, 1)[:HD[1], :HD[0]]


def glass_masks():
    import fields_f, fields_g
    m = fields_g._masks(fields_f.desert_base())
    return {k: _art(v) for k, v in m.items() if k in ("sky", "cactus", "rock", "sand", "water")}


def true_sky(m):
    """Only the open sky (connected to the top edge); enclosed bluish pockets (cactus shade, glare) are ground."""
    lbl, n = ndi.label(m["sky"])
    top = set(np.unique(lbl[0])) - {0}
    return np.isin(lbl, list(top))


def arrival(m, impact, seed, land_share=0.8):
    """Arrival time 0..1 on the art grid. Ground: geodesic distance from the impact (water fast, sand slower, rock
    slowest, noisy so the front fingers). Sky: from the nearest ground below it, climbing (the white-fire haze)."""
    sky = true_sky(m)
    n = noise((AW, AH), 6, seed, 3)
    speed = np.full((AH, AW), 0.42, np.float32)                 # sand
    speed[m["water"]] = 1.0                                     # the old flood conducts the flash
    speed[m["rock"]] = 0.26
    speed[m["cactus"]] = 0.3
    speed *= 0.55 + 0.9 * n                                     # fingering
    cost = 1.0 / np.maximum(speed, 0.05)
    cost[sky] = np.inf
    ix, iy = int(impact[0] / 2), int(impact[1] / 2)
    if sky[iy, ix]:
        raise ValueError("impact in the sky")
    mcp = MCP_Geometric(cost, fully_connected=True)
    dist, _ = mcp.find_costs([(iy, ix)])
    land = np.isfinite(dist)
    lmax = np.percentile(dist[land], 97)
    T = np.where(land, dist / lmax * land_share, 0)
    # sky: arrival of the nearest ground pixel + climb, rescaled so the top of the sky arrives at 1.0
    dsky, (ny, nx) = ndi.distance_transform_edt(~land, return_indices=True)
    base = T[ny, nx]
    sn = noise((AW, AH), 12, seed + 7, 2)
    climb = dsky * (0.8 + 0.4 * sn)
    rate = (1.0 - np.percentile(base[~land], 50)) / max(np.percentile(climb[~land], 98), 1)
    Ts = base + climb * rate
    Ts = ndi.gaussian_filter(np.where(land, T, Ts), 3)              # no Voronoi seams in the haze front
    T = np.where(land, T, Ts)
    crack_cost = 1.0 / np.maximum(speed, 0.05) * (0.25 + 3.0 * noise((AW, AH), 2, seed + 11, 2) ** 3)
    crack_cost[sky] = np.inf
    cmcp = MCP_Geometric(crack_cost, fully_connected=True)
    cmcp.find_costs([(iy, ix)])
    return np.clip(T, 0, 1), cmcp, land


def crack_network(m, mcp, T, land, impact, seed, targets=70):
    """Union of cheapest jagged paths from the impact to points spread over the glass (1 art px wide)."""
    rng = np.random.RandomState(seed)
    ok = land & (T > 0.08) & (T < 0.78)
    w = np.where(m["water"], 3.0, 1.0)[ok]
    cand = np.argwhere(ok)
    pick = cand[rng.choice(len(cand), size=min(targets, len(cand)), replace=False, p=w / w.sum())]
    net = np.zeros((AH, AW), bool)
    for (y, x) in pick:
        for (py, px) in mcp.traceback((int(y), int(x))):
            net[py, px] = True
    # keep it a web of hairlines, not a blob: drop the thick hub right at the impact
    ix, iy = int(impact[0] / 2), int(impact[1] / 2)
    yy, xx = np.mgrid[0:AH, 0:AW]
    net &= ((xx - ix) ** 2 + ((yy - iy) * 2.2) ** 2) > 9 ** 2
    return net


def steam_points(m, band, k, rng, per=5):
    """Up to `per` well-spread points (room units) where band k crosses the old water (else any ground)."""
    sel = np.argwhere((band == k) & m["water"])
    if len(sel) < 8:
        sel = np.argwhere((band == k) & ~m["sky"])
    if not len(sel):
        return []
    pts = []
    for _ in range(per * 6):
        y, x = sel[rng.randrange(len(sel))]
        if all((x - px) ** 2 + (y - py) ** 2 > 40 ** 2 for px, py in pts):
            pts.append((x, y))
        if len(pts) >= per:
            break
    return [[round(float(x) * 2 / 2.25, 1), round(float(y) * 2 / 2.25, 1)] for x, y in pts]


def soft_glow(r, col, levels=6):
    s = 2 * r
    ys, xs = np.mgrid[0:s, 0:s].astype(np.float32)
    d = np.sqrt((xs - r + 0.5) ** 2 + (ys - r + 0.5) ** 2) / r
    a = np.clip(1 - d, 0, 1) ** 1.7
    a = np.round(a * levels) / levels
    out = np.zeros((s, s, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = a * 255
    return img(out)


def heat_ring(rx, ry, col):
    W, H = 2 * rx + 8, 2 * ry + 8
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xs - W / 2) / rx) ** 2 + ((ys - H / 2) / ry) ** 2)
    a = np.clip(1 - np.abs(d - 1) * 14, 0, 1)
    a = np.round(a * 4) / 4
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = a * 255
    # pixel-art: 2x2 blocks
    im = img(out).resize((W // 2, H // 2), Image.NEAREST).resize((W // 2 * 2, H // 2 * 2), Image.NEAREST)
    return im


def puff_sheet(cells=3, w=40, h=30, seed=5):
    """Steam puffs (art px 2x2): soft lumpy cloud, light top, shaded base, translucent rim."""
    rng = random.Random(seed)
    out = Image.new("RGBA", (w * cells, h))
    pal = [(250, 255, 252), (228, 242, 236), (200, 222, 214)]
    for c in range(cells):
        aw, ah = w // 2, h // 2
        ys, xs = np.mgrid[0:ah, 0:aw].astype(np.float32)
        v = np.full((ah, aw), -1.0)
        for _ in range(5):
            cx, cy = rng.uniform(aw * 0.3, aw * 0.7), rng.uniform(ah * 0.45, ah * 0.65)
            r = rng.uniform(aw * 0.18, aw * 0.3)
            d2 = ((xs - cx) / r) ** 2 + ((ys - cy) / (r * 0.85)) ** 2
            v = np.where(d2 < 1, np.maximum(v, 0.6 - 0.5 * (ys - cy) / r), v)
        inside = v > -0.5
        band = np.where(v > 0.75, 0, np.where(v > 0.45, 1, 2))
        a = np.zeros((ah, aw, 4), np.float32)
        a[..., :3] = np.array(pal, np.float32)[band]
        edge = inside & ~ndi.binary_erosion(inside)
        a[..., 3] = np.where(inside, np.where(edge, 130, 225), 0)
        cell = img(a).resize((w, h), Image.NEAREST)
        out.alpha_composite(cell, (c * w, 0))
    return out


def build_glass_quench(verbose=True):
    room_p = os.path.join(OUT, "battlebg", "field_glass_dunes_hd.png")
    room = np.asarray(Image.open(room_p).convert("RGBA"))
    m = glass_masks()
    # the room's own amber cooling seams (exact colour the builder paints)
    seams = _art(np.all(room[..., :3] == (255, 176, 70), -1))
    base = os.path.join(TR_DIR, "glass_quench")
    data = {"art": "field_glass_dunes", "bands": BANDS, "impacts": {}}
    files = []
    for tag, pt, seed in (("foe", FOE, 901), ("player", PLAYER, 911)):
        T, mcp, land = arrival(m, pt, seed)
        band = np.minimum((T * BANDS).astype(int), BANDS - 1)
        net = crack_network(m, mcp, T, land, pt, seed + 1)
        d = os.path.join(base, tag)
        os.makedirs(d, exist_ok=True)
        rng = random.Random(seed)
        steam = []
        bandhd = _hd(band)
        nethd, seamhd = _hd(net), _hd(seams)
        skyhd = _hd(~land)
        That = _hd(T)
        rimnoise = _hd(noise((AW, AH), 3, seed + 21, 1))
        for k in range(BANDS):
            msk = bandhd == k
            rv = np.where(msk[..., None], room, 0).astype(np.uint8)        # transparent = (0,0,0,0): small PNGs
            rv[..., 3] = np.where(msk, 255, 0)
            Image.fromarray(rv, "RGBA").save(os.path.join(d, "rv%02d.png" % k), optimize=True)
            # heat: ground only. A white-hot rim on the band's leading (outer) edge, a dim amber body behind it
            ground = msk & ~skyhd
            lead = ground & (That >= (k + 1 - RIM) / BANDS) & (rimnoise > 0.25)
            hk = np.zeros(room.shape, np.uint8)
            hk[ground] = (255, 168, 78, 110)
            hk[lead] = WHITE_HOT + (int(255 * (1 - 0.45 * k / (BANDS - 1))),)   # farther fronts glow less
            Image.fromarray(hk, "RGBA").save(os.path.join(d, "hk%02d.png" % k), optimize=True)
            lt = np.zeros(room.shape, np.uint8)
            lt[nethd & msk] = (190, 255, 236, 255)                 # white-cyan hairlines through the glass
            lt[seamhd & msk] = (255, 196, 96, 255)                 # the cooling seams flare amber
            Image.fromarray(lt, "RGBA").save(os.path.join(d, "lt%02d.png" % k), optimize=True)
            files += ["transitions/glass_quench/%s/%s%02d.png" % (tag, kind, k) for kind in ("rv", "hk", "lt")]
            steam.append(steam_points(m, band, k, rng))
        data["impacts"][tag] = {"point": [round(float(pt[0]) / 2.25, 2), round(float(pt[1]) / 2.25, 2)], "steam": steam}
        if verbose:
            share = [int((band == k).sum()) for k in range(BANDS)]
            print(tag, "band sizes (art px):", share, "crack px:", int(net.sum()))
    soft_glow(90, WHITE_HOT).save(os.path.join(base, "glow.png"), optimize=True)
    heat_ring(150, 34, (255, 236, 200)).save(os.path.join(base, "ring.png"), optimize=True)
    puff_sheet().save(os.path.join(base, "puff.png"), optimize=True)
    files += ["transitions/glass_quench/glow.png", "transitions/glass_quench/ring.png", "transitions/glass_quench/puff.png"]
    return data, files


def write_ruby(staged):
    from rubygen import rb, S
    lines = [
        "#===============================================================================",
        "# Prismfall EBDX Bridge - GENERATED staged-transition data. Do not edit by hand:",
        "# rebuild with `python3 -I art/battlebacks/transitions.py`.",
        "# STAGED_ART[:name] = { :art (the new room the bands were cut from), :dir, :bands,",
        "#   :impacts => { :foe/:player => { :point [room x, y], :steam [per band: [[x, y], ...]] } } }",
        "# Runtime: 008_Bridge_Transitions.rb. Timing and colours: STAGED_TRANSITIONS (001).",
        "#===============================================================================",
        "module PrismfallEBDX",
        "  STAGED_ART = {",
    ]
    for name, d in staged.items():
        imp = {S(k): {S("point"): v["point"], S("steam"): v["steam"]} for k, v in d["impacts"].items()}
        spec = {S("art"): d["art"], S("dir"): "Graphics/EBDX/Battlebacks/transitions/" + name + "/",
                S("bands"): d["bands"], S("impacts"): imp}
        lines.append("    :%s => %s," % (name, rb(spec, 2)))
    lines += ["  }", "end", ""]
    open(RB_OUT, "w", encoding="utf-8").write("\n".join(lines))
    print("wrote", RB_OUT)


def build():
    data, files = build_glass_quench()
    write_ruby({"glass_quench": data})
    # credits row (docs/CREDITS.md backdrop table is generated from origins.json)
    import build_backdrops as B
    ORIG = B.ORIGINS
    origins = json.load(open(ORIG)) if os.path.exists(ORIG) else {}
    from fields_a import OWN
    from fields_f import AVEON
    origins["TRANSITION_GLASS_QUENCH"] = {
        "sources": [[AVEON, "the GLASS_DUNES room's own pixels, cut into reveal bands"],
                    [OWN, "flood/desert -> glass staged transition: arrival-time bands from the impact, white-hot "
                          "front, crackle of light, steam puffs, impact glow and heat ring"]],
        "files": sorted(files)}
    json.dump(origins, open(ORIG, "w"), indent=1, sort_keys=True)
    B.write_credits(origins)


if __name__ == "__main__":
    build()
