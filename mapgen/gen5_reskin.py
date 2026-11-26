#!/usr/bin/env python3
"""gen5_reskin.py — Deterministic Gen 3 -> True Gen 5 B2W2 Tileset & Autotile Remaster Engine.

100% tile-index-preserving, dimension-preserving, alpha-mask-preserving visual upgrade
for all 8 active Prismfall physical tilesets and all active RMXP autotiles.

Usage:
  /usr/bin/python3 mapgen/gen5_reskin.py --src-roots maps_out/Graphics /home/antigravity/pf_engine_run/game/Graphics \
      --out-dirs graphics art/out/Graphics --verify
"""
import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

TILESETS_8 = [
    "PF Rejuv",
    "Prismfall Interior",
    "PF Rejuv Halls",
    "Prismfall City",
    "Poke Centre interior",
    "Mart interior",
    "Interior general",
    "Gyms interior",
]

STOCK_SHEETS_WITH_RED_X = {
    "Poke Centre interior",
    "Mart interior",
    "Interior general",
    "Gyms interior",
}

AUTOTILES_ALL = [
    "RJ Dirt",
    "RJ DirtDark",
    "PF Saltmere Cobbles",
    "PF Saltmere Flags",
    "PF Packed Snow",
    "PF Gravel Spring",
    "RJ KristilineDirt",
    "RJ Gravel(G)",
    "Tall Grass Flowers 2",
    "RJ Ocean",
    "RJ Sea deep",
    "RJ Sea(Grass)",
    "RB Still water snow",
    "RJ Sand shore",
    "RJ Sand shore_2",
    "PF Frozen Pond",
    "PF Lock Water",
    "water2",
    "RJ KristilineWatersFrozen",
    "PF Sea Cave",
    "PF Salt Lake",
    "PF Magma",
    "RJ Waterfall",
    "RJ Waterfall bottom",
    "RJ Waterfall crest",
    "PF Cave Pool",
    "RJ Sea",
    "RJ Still water",
    "RJ Hoenn Sea",
    "RJ Dirt Route 4",
    "RJ Dirt Route 5",
    "Bleed grass",
    "Bleed water",
    "Lava",
    "Lavafall",
]


# ---------------------------------------------------------------------------
# Fast Vectorized RGB <-> HSV Utilities (float32 in [0, 1], H in [0, 360))
# ---------------------------------------------------------------------------
def rgb_to_hsv(rgb: np.ndarray):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    df = mx - mn
    h = np.zeros_like(mx)
    nz = df > 1e-6
    rm = nz & (mx == r)
    gm = nz & (mx == g) & (~rm)
    bm = nz & (~rm) & (~gm)
    h[rm] = (60.0 * ((g[rm] - b[rm]) / df[rm])) % 360.0
    h[gm] = (60.0 * ((b[gm] - r[gm]) / df[gm]) + 120.0) % 360.0
    h[bm] = (60.0 * ((r[bm] - g[bm]) / df[bm]) + 240.0) % 360.0
    s = np.where(mx > 1e-6, df / np.maximum(mx, 1e-6), 0.0)
    return h, s, mx


def hsv_to_rgb(h: np.ndarray, s: np.ndarray, v: np.ndarray) -> np.ndarray:
    h = np.mod(h, 360.0)
    s = np.clip(s, 0.0, 1.0)
    v = np.clip(v, 0.0, 1.0)
    c = v * s
    x = c * (1.0 - np.abs((h / 60.0) % 2.0 - 1.0))
    m = v - c
    z = np.zeros_like(h)
    hi = (h // 60.0).astype(np.int32) % 6
    r = np.choose(hi, [c, x, z, z, x, c]) + m
    g = np.choose(hi, [x, c, c, x, z, z]) + m
    b = np.choose(hi, [z, z, x, c, c, x]) + m
    return np.stack([r, g, b], axis=-1)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / max(edge1 - edge0, 1e-6), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def hue_dist(h: np.ndarray, target: float) -> np.ndarray:
    d = np.abs(h - target) % 360.0
    return np.minimum(d, 360.0 - d)


def lerp_hue(h0: np.ndarray, h1: float, w: np.ndarray) -> np.ndarray:
    diff = ((h1 - h0 + 180.0) % 360.0) - 180.0
    return (h0 + diff * w) % 360.0


def lerp_hue_arr(h0: np.ndarray, h1: np.ndarray, w: np.ndarray) -> np.ndarray:
    diff = ((h1 - h0 + 180.0) % 360.0) - 180.0
    return (h0 + diff * w) % 360.0


def apply_s_curve(v: np.ndarray, strength: float = 0.22, pivot: float = 0.48) -> np.ndarray:
    """Crisp B2W2 value contrast expansion around pivot."""
    c = np.where(
        v < pivot,
        pivot * np.power(np.clip(v / max(pivot, 1e-5), 0.0, 1.0), 1.0 + strength),
        1.0 - (1.0 - pivot) * np.power(np.clip((1.0 - v) / max(1.0 - pivot, 1e-5), 0.0, 1.0), 1.0 + strength),
    )
    return np.clip(c, 0.0, 1.0)


def red_x_placeholder_mask(arr: np.ndarray) -> np.ndarray:
    """Detect stock Essentials red-X empty placeholder 32x32 tiles so they remain untouched."""
    H, W = arr.shape[:2]
    mask = np.zeros((H, W), dtype=bool)
    for ty in range(0, H - 31, 32):
        for tx in range(0, W - 31, 32):
            tile = arr[ty:ty + 32, tx:tx + 32]
            vis = tile[..., 3] > 200
            if vis.mean() < 0.8:
                continue
            r, g, b = tile[..., 0], tile[..., 1], tile[..., 2]
            is_white = (r > 245) & (g > 245) & (b > 245)
            is_red = (r > 235) & (g < 25) & (b < 25)
            if is_white.mean() > 0.65 and is_red.mean() > 0.08 and (is_white | is_red).mean() > 0.90:
                mask[ty:ty + 32, tx:tx + 32] = True
    return mask


# ---------------------------------------------------------------------------
# MODULE 1: Unified Gen 5 B2W2 Biome Shaders
# ---------------------------------------------------------------------------
def shade_outdoor_nature(rgb_u8: np.ndarray, alpha: np.ndarray, warm_timber: bool = False) -> np.ndarray:
    """Unified Gen 5 B2W2 Floccesy/Aspertia Outdoor Nature & Architecture Shader.

    Applied IDENTICALLY to sh/gl/ak/rb4/ap, grass-fringed autotiles, and outdoor stamps
    so every grass-to-path and grass-to-water seam stays 100.00% bit-exact.
    """
    rgb = rgb_u8.astype(np.float32) / 255.0
    h, s, v = rgb_to_hsv(rgb)
    h_new, s_new, v_new = h.copy(), s.copy(), v.copy()

    # 1. Gen 3 Mint / Seafoam Grass -> B2W2 Floccesy/Aspertia Olive-Emerald Grass
    # Target anchor: RGB(112,200,160) -> RGB(92,138,58) (exact match to proof 103!)
    mint_h = 1.0 - smoothstep(16.0, 32.0, hue_dist(h, 152.0))
    mint_s = smoothstep(0.14, 0.24, s) * (1.0 - smoothstep(0.68, 0.85, s))
    mint_v = smoothstep(0.46, 0.62, v)
    w_mint = mint_h * mint_s * mint_v

    grass_h = 92.0 + 6.0 * (1.0 - smoothstep(0.55, 0.85, v))
    grass_s = np.clip(s * 1.24 + 0.04, 0.36, 0.68)
    grass_v = np.clip(0.14 + v * 0.525, 0.22, 0.72)

    h_new = lerp_hue_arr(h_new, np.full_like(h, grass_h), w_mint)
    s_new = s_new * (1.0 - w_mint) + grass_s * w_mint
    v_new = v_new * (1.0 - w_mint) + grass_v * w_mint

    # 1b. Dirt-path grass rim highlight (e.g. RGB(168,216,160) on RJ DirtDark/Dirt/Gravel):
    # pull down from pale highlighter mint into warm B2W2 sunlit olive blade edge (matches grass seamlessly!)
    rim_h = 1.0 - smoothstep(14.0, 24.0, hue_dist(h, 111.0))
    rim_s = smoothstep(0.18, 0.24, s) * (1.0 - smoothstep(0.32, 0.40, s))
    rim_v = smoothstep(0.76, 0.84, v)
    w_rim = rim_h * rim_s * rim_v * (1.0 - w_mint)
    h_new = lerp_hue_arr(h_new, np.full_like(h, 90.0), w_rim)
    s_new = s_new * (1.0 - w_rim) + np.clip(s * 1.95, 0.46, 0.56) * w_rim
    v_new = v_new * (1.0 - w_rim) + np.clip(v * 0.72, 0.56, 0.63) * w_rim

    # 2. Gen 3 Cartoon Foliage / Trees / Bushes / Tall Grass -> B2W2 Hue-Shifted Forest Canopies
    # Deep cool pine-teal shadows (V<0.42) -> Lush emerald mid -> Warm sunlit olive crowns (V>0.62)
    fol_h = 1.0 - smoothstep(32.0, 48.0, hue_dist(h, 134.0))
    fol_s = smoothstep(0.18, 0.30, s)
    w_fol = fol_h * fol_s * (1.0 - w_mint) * (1.0 - w_rim)

    w_dark = 1.0 - smoothstep(0.20, 0.46, v)
    w_bright = smoothstep(0.54, 0.82, v)
    fol_target_h = (
        w_dark * 182.0                               # deep pine-teal blue underside!
        + (1.0 - w_dark) * (1.0 - w_bright) * 148.0  # lush forest emerald midtone
        + w_bright * 98.0                            # warm sunlit golden-olive crown!
    )
    fol_target_s = np.clip(
        w_dark * np.clip(s * 0.96, 0.38, 0.76)
        + (1.0 - w_dark) * (1.0 - w_bright) * np.clip(s * 0.94, 0.34, 0.72)
        + w_bright * np.clip(s * 0.78, 0.38, 0.64),
        0.0, 1.0,
    )
    fol_target_v = np.clip(
        w_dark * (v * 0.76)
        + (1.0 - w_dark) * (1.0 - w_bright) * (v * 0.82)
        + w_bright * (0.28 + v * 0.48),
        0.04, 0.79,
    )
    h_new = lerp_hue_arr(h_new, fol_target_h, w_fol)
    s_new = s_new * (1.0 - w_fol) + fol_target_s * w_fol
    v_new = v_new * (1.0 - w_fol) + fol_target_v * w_fol

    # 3. Earth, Cliffs, Dirt & Rustic Wood (Warm ochre/brown band H in [14, 56])
    earth_h = 1.0 - smoothstep(18.0, 28.0, hue_dist(h, 33.0))
    earth_s = smoothstep(0.08, 0.16, s) * (1.0 - smoothstep(0.76, 0.92, s))
    w_earth = earth_h * earth_s * (1.0 - w_mint) * (1.0 - w_fol)

    if warm_timber:
        # Transform washed-out grey-taupe lodges (gl/sh/wb/th/wh) into rich B2W2 cedar & walnut timber!
        is_taupe = earth_h * smoothstep(0.08, 0.14, s) * (1.0 - smoothstep(0.36, 0.48, s)) * smoothstep(0.16, 0.24, v)
        cedar_h = np.where(v > 0.65, 31.0, 25.0)
        cedar_s = np.clip(s * 2.02 + 0.13, 0.30, 0.58)
        cedar_v = apply_s_curve(v * 0.93, strength=0.32, pivot=0.46)
        h_new = lerp_hue_arr(h_new, cedar_h, is_taupe)
        s_new = s_new * (1.0 - is_taupe) + cedar_s * is_taupe
        v_new = v_new * (1.0 - is_taupe) + cedar_v * is_taupe
        w_earth_rem = w_earth * (1.0 - is_taupe)
    else:
        w_earth_rem = w_earth

    e_h = np.where(v < 0.30, lerp_hue(h, 16.0, 0.35), lerp_hue(h, 29.0, 0.25))
    e_s = np.clip(s * 1.15 + 0.03, 0.0, 0.78)
    e_v = apply_s_curve(v * 0.93, strength=0.26, pivot=0.48)
    h_new = lerp_hue_arr(h_new, e_h, w_earth_rem)
    s_new = s_new * (1.0 - w_earth_rem) + e_s * w_earth_rem
    v_new = v_new * (1.0 - w_earth_rem) + e_v * w_earth_rem

    # 4. Flowers, Blossoms, Red/Blue/Gold Accents & Cool Stone
    w_other = np.clip(1.0 - w_mint - w_fol - w_earth, 0.0, 1.0)
    w_stone = w_other * (1.0 - smoothstep(0.08, 0.16, s)) * smoothstep(0.12, 0.22, v)
    st_v = apply_s_curve(v * 0.93, strength=0.24, pivot=0.50)
    h_new = lerp_hue_arr(h_new, np.full_like(h, 224.0), w_stone * 0.42)
    s_new = s_new * (1.0 - w_stone) + np.clip(s + 0.06, 0.0, 0.16) * w_stone
    v_new = v_new * (1.0 - w_stone) + st_v * w_stone

    w_vivid = w_other * (1.0 - w_stone) * smoothstep(0.20, 0.35, s)
    v_new = v_new * (1.0 - w_vivid) + apply_s_curve(v * 0.96, strength=0.18, pivot=0.52) * w_vivid
    s_new = s_new * (1.0 - w_vivid) + np.clip(s * 1.08, 0.0, 0.94) * w_vivid

    out = hsv_to_rgb(h_new, s_new, v_new)

    # 5. Global B2W2 Cool-Shadow Anchor
    w_outline = (1.0 - smoothstep(0.06, 0.22, v)) * (alpha > 128)
    out[..., 0] = out[..., 0] * (1.0 - 0.14 * w_outline)
    out[..., 1] = out[..., 1] * (1.0 - 0.06 * w_outline)
    out[..., 2] = np.clip(out[..., 2] * (1.0 + 0.12 * w_outline) + 0.02 * w_outline, 0.0, 1.0)

    return np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8)


def shade_snow_biome(rgb_u8: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Authentic Gen 5 B2W2 Unova Winter (Icirrus / Giant Chasm) Shader for kf & snow autotiles."""
    rgb = rgb_u8.astype(np.float32) / 255.0
    h, s, v = rgb_to_hsv(rgb)
    h_new, s_new, v_new = h.copy(), s.copy(), v.copy()

    # 1. Snow & Frost Highlights/Shadows (low-sat cool/lavender/white pixels)
    w_snow = (1.0 - smoothstep(0.18, 0.34, s)) * smoothstep(0.32, 0.45, v)
    w_hi = smoothstep(0.84, 0.95, v)
    w_mid = w_snow * (1.0 - w_hi)
    # Richer icy cerulean-periwinkle snow shadows (distinguishes paths clearly from Bleed violet frost!)
    snow_h = np.where(hue_dist(h, 275.0) < 35.0, lerp_hue(h, 252.0, 0.40), lerp_hue(h, 218.0, 0.72))
    h_new = lerp_hue_arr(h_new, snow_h, w_mid)
    s_new = s_new * (1.0 - w_mid) + np.clip(s * 1.36 + 0.07, 0.12, 0.40) * w_mid
    v_new = v_new * (1.0 - w_mid) + apply_s_curve(v * 0.91, strength=0.34, pivot=0.66) * w_mid
    # Crisp luminous snow highlights
    h_new = lerp_hue_arr(h_new, np.full_like(h, 204.0), w_snow * w_hi * 0.55)
    s_new = s_new * (1.0 - w_snow * w_hi) + np.clip(s * 0.55, 0.02, 0.09) * (w_snow * w_hi)
    v_new = v_new * (1.0 - w_snow * w_hi) + np.clip(v * 1.04, 0.0, 0.99) * (w_snow * w_hi)

    # 2. Bleed Purple/Violet Trees & Crystals -> Rich Jewel Amethyst-Plum
    w_purp = (1.0 - smoothstep(28.0, 44.0, hue_dist(h, 285.0))) * smoothstep(0.20, 0.34, s)
    h_new = lerp_hue_arr(h_new, np.where(v < 0.42, 266.0, 294.0), w_purp * 0.55)
    s_new = s_new * (1.0 - w_purp) + np.clip(s * 1.22, 0.0, 0.94) * w_purp
    v_new = v_new * (1.0 - w_purp) + apply_s_curve(v * 0.88, strength=0.30, pivot=0.45) * w_purp

    # 3. Arctic Teal/Blue Pines & Ice Cliffs -> Deep Sapphire-Spruce B2W2 Contrast
    w_ice = (1.0 - smoothstep(28.0, 42.0, hue_dist(h, 202.0))) * smoothstep(0.22, 0.36, s) * (1.0 - w_snow)
    h_new = lerp_hue_arr(h_new, np.where(v < 0.45, 214.0, 194.0), w_ice * 0.55)
    s_new = s_new * (1.0 - w_ice) + np.clip(s * 1.20, 0.0, 0.90) * w_ice
    v_new = v_new * (1.0 - w_ice) + apply_s_curve(v * 0.86, strength=0.32, pivot=0.48) * w_ice

    # 4. Warm Alpine Chalet Timber / Torches / Lanterns
    w_warm = (1.0 - smoothstep(22.0, 34.0, hue_dist(h, 30.0))) * smoothstep(0.18, 0.30, s)
    s_new = s_new * (1.0 - w_warm) + np.clip(s * 1.26, 0.0, 0.94) * w_warm
    v_new = v_new * (1.0 - w_warm) + apply_s_curve(v * 0.95, strength=0.22, pivot=0.50) * w_warm

    # 5. Any green trees in kf edge transition -> unified B2W2 outdoor foliage
    w_grn = (1.0 - smoothstep(24.0, 38.0, hue_dist(h, 140.0))) * smoothstep(0.20, 0.32, s) * (1.0 - w_ice)
    if np.any(w_grn > 0.01):
        nat = shade_outdoor_nature(rgb_u8, alpha, warm_timber=False).astype(np.float32) / 255.0
        out = hsv_to_rgb(h_new, s_new, v_new)
        out = out * (1.0 - w_grn[..., None]) + nat * w_grn[..., None]
    else:
        out = hsv_to_rgb(h_new, s_new, v_new)

    w_dark = (1.0 - smoothstep(0.08, 0.28, v)) * (alpha > 128)
    out[..., 0] = out[..., 0] * (1.0 - 0.16 * w_dark)
    out[..., 1] = out[..., 1] * (1.0 - 0.08 * w_dark)
    out[..., 2] = np.clip(out[..., 2] * (1.0 + 0.14 * w_dark) + 0.03 * w_dark, 0.0, 1.0)
    return np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8)


def shade_cave_strata(rgb_u8: np.ndarray, alpha: np.ndarray, mode: str = "salt") -> np.ndarray:
    """Chargestone / Mistralton 3D Slate-Quartz Cave Shader (Brinecut S_*, Gullcry L_*, Cindervault E_*)."""
    rgb = rgb_u8.astype(np.float32) / 255.0
    h, s, v = rgb_to_hsv(rgb)
    h_new, s_new, v_new = h.copy(), s.copy(), v.copy()

    is_wood = (1.0 - smoothstep(16.0, 24.0, hue_dist(h, 28.0))) * smoothstep(0.28, 0.38, s) * (1.0 - smoothstep(0.60, 0.72, v))
    is_crystal = smoothstep(0.32, 0.44, s) * (1.0 - is_wood)
    is_rock = (1.0 - is_crystal) * (1.0 - is_wood) * smoothstep(0.04, 0.10, v)

    if mode == "salt":
        # Chargestone two-tone: deep cool slate-violet rock shadows paired with warm rose-white
        # crystalline salt crust on brick faces, upper ledges, and drained salt ridges.
        w_lip = smoothstep(0.66, 0.84, v)
        base_h = 238.0 + 18.0 * smoothstep(0.32, 0.72, v)
        target_h = lerp_hue_arr(base_h, np.full_like(h, 336.0), w_lip)
        target_s = 0.32 * (1.0 - w_lip) + (0.16 + 0.04 * (1.0 - smoothstep(0.84, 0.96, v))) * w_lip
        target_v = np.clip(0.11 + 0.50 * np.power(v, 1.42), 0.08, 0.64)
        salt_v = np.clip(0.68 + 0.24 * smoothstep(0.66, 0.96, v), 0.68, 0.92)
        target_v = target_v * (1.0 - w_lip) + salt_v * w_lip
        w_rim = smoothstep(0.90, 0.98, v)
        target_v = target_v * (1.0 - w_rim) + np.clip(v * 0.94, 0.84, 0.95) * w_rim
    elif mode == "limestone":
        target_h = np.full_like(h, 212.0)
        target_s = np.clip(s * 0.6 + 0.24, 0.16, 0.36)
        target_v = np.clip(0.12 + 0.56 * np.power(v, 1.35), 0.09, 0.74)
    else:
        target_h = np.where(v > 0.72, 18.0, 265.0)
        target_s = np.where(v > 0.72, 0.28, 0.24)
        target_v = np.clip(0.09 + 0.48 * np.power(v, 1.50), 0.07, 0.62)

    h_new = lerp_hue_arr(h_new, target_h, is_rock)
    s_new = s_new * (1.0 - is_rock) + target_s * is_rock
    v_new = v_new * (1.0 - is_rock) + target_v * is_rock

    h_new = lerp_hue_arr(h_new, np.full_like(h, 25.0), is_wood * 0.4)
    s_new = s_new * (1.0 - is_wood) + np.clip(s * 1.18, 0.0, 0.76) * is_wood
    v_new = v_new * (1.0 - is_wood) + apply_s_curve(v * 0.84, strength=0.25, pivot=0.42) * is_wood

    s_new = s_new * (1.0 - is_crystal) + np.clip(s * 1.24, 0.0, 0.96) * is_crystal
    v_new = v_new * (1.0 - is_crystal) + np.clip(apply_s_curve(v * 1.05, strength=0.20, pivot=0.45), 0.0, 1.0) * is_crystal

    out = hsv_to_rgb(h_new, s_new, v_new)

    w_crev = (1.0 - smoothstep(0.05, 0.20, v)) * (alpha > 128)
    out[..., 0] = out[..., 0] * (1.0 - 0.18 * w_crev)
    out[..., 1] = out[..., 1] * (1.0 - 0.15 * w_crev)
    out[..., 2] = np.clip(out[..., 2] * (1.0 + 0.18 * w_crev) + 0.03 * w_crev, 0.0, 1.0)
    return np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8)


def shade_lumen_metropolis(rgb_u8: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Castelia / Nimbasa / Plasma Frigate Shader for Lumen City & Meridian Spire (lm_*, lb_*, Z/Y/Q_*)."""
    rgb = rgb_u8.astype(np.float32) / 255.0
    h, s, v = rgb_to_hsv(rgb)
    h_new, s_new, v_new = h.copy(), s.copy(), v.copy()

    # 1. Warm beige/cream granite pavement & limestone walls -> crisp Castelia cool-warm granite
    is_stone = (1.0 - smoothstep(0.14, 0.24, s)) * smoothstep(0.24, 0.34, v)
    st_h = np.where(v < 0.68, 224.0, 38.0)
    st_s = np.where(v < 0.68, np.clip(s * 0.45 + 0.10, 0.07, 0.17), np.clip(s * 0.60, 0.03, 0.10))
    st_v = apply_s_curve(v * 0.87, strength=0.36, pivot=0.58)
    h_new = lerp_hue_arr(h_new, st_h, is_stone)
    s_new = s_new * (1.0 - is_stone) + st_s * is_stone
    v_new = v_new * (1.0 - is_stone) + st_v * is_stone

    # 2. Terracotta brick roofs (warm red-orange)
    is_brick = (1.0 - smoothstep(18.0, 28.0, hue_dist(h, 12.0))) * smoothstep(0.28, 0.42, s)
    h_new = lerp_hue_arr(h_new, np.where(v < 0.50, 8.0, 16.0), is_brick * 0.55)
    s_new = s_new * (1.0 - is_brick) + np.clip(s * 1.18, 0.0, 0.86) * is_brick
    v_new = v_new * (1.0 - is_brick) + apply_s_curve(v * 0.86, strength=0.34, pivot=0.50) * is_brick

    # 3. Warm glowing windows / golden astrolabe / brass trim -> luminous radiant amber-gold!
    is_gold = (1.0 - smoothstep(14.0, 22.0, hue_dist(h, 46.0))) * smoothstep(0.26, 0.40, s)
    h_new = lerp_hue_arr(h_new, np.where(v < 0.55, 32.0, 42.0), is_gold * 0.50)
    s_new = s_new * (1.0 - is_gold) + np.clip(s * 1.24, 0.0, 0.94) * is_gold
    v_new = v_new * (1.0 - is_gold) + np.clip(apply_s_curve(v * 1.08, strength=0.22, pivot=0.46), 0.0, 1.0) * is_gold

    # 4. Slate mansard roofs & steel Spire panels
    is_steel = (1.0 - smoothstep(26.0, 38.0, hue_dist(h, 220.0))) * smoothstep(0.12, 0.24, s) * (1.0 - is_stone)
    is_cyan_glow = (1.0 - smoothstep(16.0, 24.0, hue_dist(h, 192.0))) * smoothstep(0.42, 0.58, s) * smoothstep(0.62, 0.76, v)
    w_st = is_steel * (1.0 - is_cyan_glow)
    s_new = s_new * (1.0 - w_st) + np.clip(s * 1.22, 0.0, 0.80) * w_st
    v_new = v_new * (1.0 - w_st) + apply_s_curve(v * 0.86, strength=0.32, pivot=0.45) * w_st
    s_new = s_new * (1.0 - is_cyan_glow) + np.clip(s * 1.18, 0.0, 0.96) * is_cyan_glow
    v_new = v_new * (1.0 - is_cyan_glow) + np.clip(v * 1.10, 0.0, 1.0) * is_cyan_glow

    # 5. Verdigris copper roofs & park hedges
    is_grn = (1.0 - smoothstep(32.0, 44.0, hue_dist(h, 148.0))) * smoothstep(0.18, 0.30, s) * (1.0 - is_cyan_glow)
    if np.any(is_grn > 0.01):
        g_h = np.where(v < 0.48, 178.0, np.where(v > 0.70, 128.0, 156.0))
        h_new = lerp_hue_arr(h_new, g_h, is_grn * 0.78)
        s_new = s_new * (1.0 - is_grn) + np.clip(s * 1.16, 0.0, 0.80) * is_grn
        v_new = v_new * (1.0 - is_grn) + apply_s_curve(v * 0.78, strength=0.30, pivot=0.46) * is_grn

    out = hsv_to_rgb(h_new, s_new, v_new)

    w_dark = (1.0 - smoothstep(0.06, 0.24, v)) * (alpha > 128)
    out[..., 0] = out[..., 0] * (1.0 - 0.16 * w_dark)
    out[..., 1] = out[..., 1] * (1.0 - 0.09 * w_dark)
    out[..., 2] = np.clip(out[..., 2] * (1.0 + 0.18 * w_dark) + 0.025 * w_dark, 0.0, 1.0)
    return np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8)


def shade_interior_b2w2(rgb_u8: np.ndarray, alpha: np.ndarray, variant: str = "wood") -> np.ndarray:
    """Warm, High-Contrast Gen 5 B2W2 Interior Shader (Prismfall Interior, Halls, PokeCentre, Mart, General, Gyms)."""
    rgb = rgb_u8.astype(np.float32) / 255.0
    h, s, v = rgb_to_hsv(rgb)
    h_new, s_new, v_new = h.copy(), s.copy(), v.copy()

    if variant == "pokecentre":
        is_beige = (1.0 - smoothstep(18.0, 28.0, hue_dist(h, 46.0))) * smoothstep(0.14, 0.24, s) * smoothstep(0.55, 0.68, v)
        h_new = lerp_hue_arr(h_new, np.full_like(h, 220.0), is_beige * 0.55)
        s_new = s_new * (1.0 - is_beige) + np.clip(s * 0.28, 0.02, 0.10) * is_beige
        v_new = v_new * (1.0 - is_beige) + apply_s_curve(v * 0.96, strength=0.35, pivot=0.76) * is_beige

        is_red = (1.0 - smoothstep(20.0, 32.0, hue_dist(h, 10.0))) * smoothstep(0.32, 0.45, s)
        h_new = lerp_hue_arr(h_new, np.full_like(h, 354.0), is_red * 0.72)
        s_new = s_new * (1.0 - is_red) + np.clip(s * 1.24, 0.0, 0.90) * is_red
        v_new = v_new * (1.0 - is_red) + apply_s_curve(v * 0.92, strength=0.28, pivot=0.52) * is_red

        w_other = np.clip(1.0 - is_beige - is_red, 0.0, 1.0)
        s_new = s_new * (1.0 - w_other) + np.clip(s * 1.14, 0.0, 0.90) * w_other
        v_new = v_new * (1.0 - w_other) + apply_s_curve(v * 0.94, strength=0.24, pivot=0.50) * w_other

    elif variant == "mart":
        is_blue = (1.0 - smoothstep(24.0, 36.0, hue_dist(h, 214.0))) * smoothstep(0.28, 0.40, s)
        h_new = lerp_hue_arr(h_new, np.full_like(h, 206.0), is_blue * 0.6)
        s_new = s_new * (1.0 - is_blue) + np.clip(s * 0.88, 0.20, 0.68) * is_blue
        v_new = v_new * (1.0 - is_blue) + apply_s_curve(v * 0.92, strength=0.30, pivot=0.56) * is_blue

        w_other = 1.0 - is_blue
        s_new = s_new * (1.0 - w_other) + np.clip(s * 1.16, 0.0, 0.92) * w_other
        v_new = v_new * (1.0 - w_other) + apply_s_curve(v * 0.95, strength=0.24, pivot=0.52) * w_other

    else:
        is_wood = (1.0 - smoothstep(18.0, 28.0, hue_dist(h, 28.0))) * smoothstep(0.12, 0.22, s) * (1.0 - smoothstep(0.68, 0.82, s))
        w_light_wall = is_wood * smoothstep(0.72, 0.84, v) * (1.0 - smoothstep(0.22, 0.34, s))
        w_timber = is_wood * (1.0 - w_light_wall)

        h_new = lerp_hue_arr(h_new, np.where(v < 0.42, 22.0, 29.0), w_timber * 0.55)
        s_new = s_new * (1.0 - w_timber) + np.clip(s * 1.40 + 0.06, 0.22, 0.68) * w_timber
        v_new = v_new * (1.0 - w_timber) + apply_s_curve(v * 0.87, strength=0.33, pivot=0.48) * w_timber

        h_new = lerp_hue_arr(h_new, np.full_like(h, 36.0), w_light_wall * 0.4)
        s_new = s_new * (1.0 - w_light_wall) + np.clip(s * 0.82, 0.06, 0.18) * w_light_wall
        v_new = v_new * (1.0 - w_light_wall) + apply_s_curve(v * 0.96, strength=0.24, pivot=0.68) * w_light_wall

        is_rug = (1.0 - smoothstep(16.0, 26.0, hue_dist(h, 2.0))) * smoothstep(0.28, 0.40, s)
        h_new = lerp_hue_arr(h_new, np.full_like(h, 352.0), is_rug * 0.55)
        s_new = s_new * (1.0 - is_rug) + np.clip(s * 1.24, 0.0, 0.88) * is_rug
        v_new = v_new * (1.0 - is_rug) + apply_s_curve(v * 0.84, strength=0.30, pivot=0.45) * is_rug

        is_grn = (1.0 - smoothstep(28.0, 40.0, hue_dist(h, 134.0))) * smoothstep(0.20, 0.32, s)
        g_h = np.where(v < 0.42, 168.0, np.where(v > 0.68, 102.0, 144.0))
        h_new = lerp_hue_arr(h_new, g_h, is_grn * 0.80)
        s_new = s_new * (1.0 - is_grn) + np.clip(s * 0.96, 0.0, 0.72) * is_grn
        v_new = v_new * (1.0 - is_grn) + apply_s_curve(v * 0.86, strength=0.26, pivot=0.46) * is_grn

        w_other = np.clip(1.0 - is_wood - is_rug - is_grn, 0.0, 1.0)
        s_new = s_new * (1.0 - w_other) + np.clip(s * 1.15, 0.0, 0.90) * w_other
        v_new = v_new * (1.0 - w_other) + apply_s_curve(v * 0.92, strength=0.24, pivot=0.50) * w_other

    out = hsv_to_rgb(h_new, s_new, v_new)

    w_dark = (1.0 - smoothstep(0.06, 0.22, v)) * (alpha > 128)
    out[..., 0] = out[..., 0] * (1.0 - 0.14 * w_dark)
    out[..., 1] = out[..., 1] * (1.0 - 0.10 * w_dark)
    out[..., 2] = np.clip(out[..., 2] * (1.0 + 0.10 * w_dark) + 0.02 * w_dark, 0.0, 1.0)
    return np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# MODULE 2: Crisp 16x16-Logical Pixel-Art Micro-Detail & Hero Upgrades
# ---------------------------------------------------------------------------
def add_seamless_grass_microtexture_fast(out: np.ndarray, orig: np.ndarray, tid_list: list[int]):
    """Fast pre-filtered seamless 16x16-logical B2W2 grass blade micro-texture on flat mint-grass tiles."""
    H = orig.shape[0]
    yy, xx = np.mgrid[0:16, 0:16]
    for tid in tid_list:
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 > H:
            continue
        t_orig16 = orig[ty:ty + 32:2, tx:tx + 32:2]
        # Ultra-fast rejection (<0.01ms): mint grass has opaque alpha + G >> R + B > 120!
        if t_orig16[0, 0, 3] < 200:
            continue
        r, g, b = t_orig16[..., 0].astype(np.int16), t_orig16[..., 1].astype(np.int16), t_orig16[..., 2].astype(np.int16)
        is_mint = (t_orig16[..., 3] > 200) & (g > 165) & (b > 125) & (r < 150) & ((g - r) > 45) & ((g - b) > 15)
        if is_mint.mean() < 0.86:
            continue

        out16 = out[ty:ty + 32:2, tx:tx + 32:2].copy().astype(np.int16)
        rng = np.random.default_rng(1337 + tid * 31)
        n_blades = 3 + (tid % 3)
        for _ in range(n_blades):
            bx = int(rng.integers(1, 14))
            by = int(rng.integers(1, 14))
            if not (is_mint[by, bx] and is_mint[by, bx + 1] and is_mint[by - 1, bx]):
                continue
            out16[by, bx, :3] += np.array([-13, -15, -10])
            out16[by, bx + 1, :3] += np.array([-8, -10, -7])
            out16[by - 1, bx, :3] += np.array([10, 12, 5])
        wave = np.sin(2.0 * math.pi * (xx + (tid % 5)) / 16.0) * np.cos(2.0 * math.pi * (yy + (tid % 7)) / 16.0)
        dither_hi = (wave > 0.45) & is_mint
        dither_lo = (wave < -0.55) & is_mint
        out16[dither_hi, 0] += 5
        out16[dither_hi, 1] += 6
        out16[dither_hi, 2] += 2
        out16[dither_lo, 0] -= 6
        out16[dither_lo, 1] -= 7
        out16[dither_lo, 2] -= 4
        res = np.clip(out16, 0, 255).astype(np.uint8).repeat(2, axis=0).repeat(2, axis=1)
        res[..., 3] = out[ty:ty + 32, tx:tx + 32, 3]
        out[ty:ty + 32, tx:tx + 32] = res


def light_gl_sh_lodge_windows(out: np.ndarray, orig: np.ndarray, start_tid: int, end_tid: int):
    """Illuminate ALL 69+ Goldenleaf/Sheridan timber lodge windows (incl. Briarwick Poké Center 3077 & 3125!)
    with warm 3-tone B2W2 glowing amber hearth light!

    Detects exact neutral-grey window glass RGB(84,84,84) & RGB(97,97,97) framed by RGB(36,36,36),
    which cleanly excludes chimneys, stones, fences, and shadows with 0% false positives.
    """
    H = orig.shape[0]
    for tid in range(start_tid, end_tid):
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 > H:
            continue
        t16 = orig[ty:ty + 32:2, tx:tx + 32:2]
        r, g, b, a = t16[..., 0], t16[..., 1], t16[..., 2], t16[..., 3]
        vis = a > 200
        frame = vis & (r == 36) & (g == 36) & (b == 36)
        pane_dark = vis & (r == 84) & (g == 84) & (b == 84)
        pane_mid = vis & (r == 97) & (g == 97) & (b == 97)
        if frame.sum() < 6 or (pane_dark.sum() + pane_mid.sum()) < 6:
            continue

        cur16 = out[ty:ty + 32:2, tx:tx + 32:2].copy()
        # Rich espresso window mullions/frame
        cur16[frame, :3] = (44, 28, 20)
        # Warm glowing amber interior light!
        cur16[pane_dark, :3] = (224, 132, 42)   # rich warm upper amber glow
        cur16[pane_mid, :3] = (255, 204, 88)    # bright golden interior pane
        # Give lower-center pixels of each lit pane an extra cozy hearth highlight glint!
        pane_all = pane_dark | pane_mid
        labeled, n_cc = ndimage.label(pane_all)
        for cid, sl in enumerate(ndimage.find_objects(labeled), start=1):
            if sl is None:
                continue
            y0, y1 = sl[0].start, sl[0].stop
            x0, x1 = sl[1].start, sl[1].stop
            if y1 - y0 >= 2:
                # Bottom row of pane glows bright warm cream-gold!
                bot_m = labeled[y1 - 1, x0:x1] == cid
                cur16[y1 - 1, x0:x1][bot_m, :3] = (255, 228, 128)
            if y1 - y0 >= 3:
                # Top row slightly deeper warm burnt-amber under window top sash
                top_m = labeled[y0, x0:x1] == cid
                cur16[y0, x0:x1][top_m, :3] = (204, 110, 32)

        block = cur16.repeat(2, axis=0).repeat(2, axis=1)
        block[..., 3] = out[ty:ty + 32, tx:tx + 32, 3]
        out[ty:ty + 32, tx:tx + 32] = block


def upgrade_lumen_conservatory_dome(sheet: np.ndarray, orig_sheet: np.ndarray, lb_pc_stamp: dict):
    """Hero Upgrade for Lumen Poké Center Conservatory Dome (lb_pc):
    Gleaming faceted B2W2 ribbed sky-glass dome with crisp iron ribs, sky glint & roof cast shadow!
    """
    layer = lb_pc_stamp["layers"][2]
    w, h = 10, 2
    orig_comp = np.zeros((h * 16, w * 16, 4), dtype=np.uint8)
    cur_comp = np.zeros((h * 16, w * 16, 4), dtype=np.uint8)
    for ty in range(h):
        for tx in range(w):
            tid = layer[ty][tx]
            if tid >= 384:
                i = tid - 384
                sx, sy = (i % 8) * 32, (i // 8) * 32
                orig_comp[ty * 16:(ty + 1) * 16, tx * 16:(tx + 1) * 16] = orig_sheet[sy:sy + 32:2, sx:sx + 32:2]
                cur_comp[ty * 16:(ty + 1) * 16, tx * 16:(tx + 1) * 16] = sheet[sy:sy + 32:2, sx:sx + 32:2]

    rgb = orig_comp[..., :3].astype(np.float32) / 255.0
    h_o, s_o, v_o = rgb_to_hsv(rgb)
    glass = (orig_comp[..., 3] > 200) & (hue_dist(h_o, 200.0) < 28.0) & (s_o > 0.24) & (v_o > 0.30)
    ys, xs = np.where(glass)
    if len(xs) == 0:
        return
    cx = float(xs.mean())
    y_bot = float(ys.max())
    rx = max(12.0, float(xs.max() - xs.min()) * 0.52)
    ry = max(10.0, float(ys.max() - ys.min()) * 1.05)

    for y, x in zip(ys, xs):
        nx = (x - cx) / rx
        ny = (y - y_bot) / ry
        # Crisp curved iron dome ribs
        rib_u = abs((nx * 3.0) - round(nx * 3.0))
        horiz_rib = abs(ny + 0.44) < 0.055 or abs(ny + 0.78) < 0.055
        if rib_u < 0.075 or horiz_rib:
            cur_comp[y, x, :3] = (28, 60, 96)
            continue
        nz = math.sqrt(max(0.05, 1.0 - min(0.95, nx * nx + (ny * 0.85) ** 2)))
        lum = 0.48 + 0.46 * (-0.42 * nx - 0.56 * ny + 0.52 * nz)
        if -0.60 < nx < -0.10 and -0.84 < ny < -0.20 and abs((nx + 0.34) - (ny + 0.52) * 0.44) < 0.16:
            cur_comp[y, x, :3] = (234, 252, 255)  # sparkling sky glint!
        elif lum > 0.78:
            cur_comp[y, x, :3] = (146, 226, 254)
        elif lum > 0.58:
            cur_comp[y, x, :3] = (78, 182, 236)
        elif lum > 0.40:
            cur_comp[y, x, :3] = (46, 134, 198)
        else:
            cur_comp[y, x, :3] = (32, 96, 156)

    # Cool cast shadow on right/base of dome
    dil = ndimage.binary_dilation(glass, iterations=2) & (~glass)
    for y, x in zip(*np.where(dil)):
        if x > cx - 2 and cur_comp[y, x, 3] > 200:
            cur_comp[y, x, 0] = int(cur_comp[y, x, 0] * 0.74)
            cur_comp[y, x, 1] = int(cur_comp[y, x, 1] * 0.76)
            cur_comp[y, x, 2] = int(cur_comp[y, x, 2] * 0.88)

    for ty in range(h):
        for tx in range(w):
            tid = layer[ty][tx]
            if tid >= 384:
                i = tid - 384
                sx, sy = (i % 8) * 32, (i // 8) * 32
                block = cur_comp[ty * 16:(ty + 1) * 16, tx * 16:(tx + 1) * 16].repeat(2, axis=0).repeat(2, axis=1)
                block[..., 3] = sheet[sy:sy + 32, sx:sx + 32, 3]
                sheet[sy:sy + 32, sx:sx + 32] = block


def upgrade_lumen_paving_bevel(tile_rgba: np.ndarray, tid: int) -> np.ndarray:
    """Crisp, clean, non-busy Castelia/Nimbasa beveled granite slabs for lm_pave / lm_plaza."""
    im16 = tile_rgba[::2, ::2].copy().astype(np.int16)
    if (im16[..., 3] > 200).mean() < 0.95:
        return tile_rgba
    # Subtle, refined granite slab mortar along tile outer edge + gentle sunlit top-left bevel
    im16[0, :, :3] = np.clip(im16[0, :, :3] - np.array([15, 14, 10]), 0, 255)
    im16[:, 0, :3] = np.clip(im16[:, 0, :3] - np.array([12, 11, 8]), 0, 255)
    im16[1, 1:, :3] = np.clip(im16[1, 1:, :3] + np.array([9, 9, 8]), 0, 255)
    im16[1:, 1, :3] = np.clip(im16[1:, 1, :3] + np.array([7, 7, 6]), 0, 255)
    # Subtle warm/cool architectural slab tone variation
    sign = 1 if (tid % 2 == 0) else -1
    im16[2:15, 2:15, :3] += np.array([3 * sign, 2 * sign, 1 * sign])
    out = np.clip(im16, 0, 255).astype(np.uint8).repeat(2, axis=0).repeat(2, axis=1)
    out[..., 3] = tile_rgba[..., 3]
    return out


def upgrade_spire_sanctum_hero_tiles(out: np.ndarray, orig: np.ndarray, srjc: dict):
    """Hero upgrades for Meridian Spire & Plate Vault (Map 952, 951, 185, 190, 255):
      - lm_stair_l/m/r: 3D cool-shadowed alabaster marble stair risers + luminous treads
      - lm_sun / lm_ring / lm_core: gleaming burnished N's Castle gold astrolabe
      - lm_deep0..5: deep midnight cosmic sapphire abyss with brighter glowing star motes
      - Z_f0..3: sleek beveled dark indigo-gunmetal Plasma Frigate deck tiles
      - Q_f0..2: sleek beveled steel Plasma Frigate deck plating (replaces dot-matrix!)
      - lm_monitors: glowing holographic cyan/amber radar & waveform console
      - lm_carpet_*: rich royal crimson velvet + burnished gold filigree
    """
    H = out.shape[0]

    def tids_for_prefix(prefixes):
        s = set()
        for k, st in srjc.items():
            if any(k == p or k.startswith(p) for p in prefixes):
                for l in st.get("layers", []):
                    for r in l:
                        for t in r:
                            if t >= 384:
                                s.add(t)
        return sorted(s)

    # 1. Grand Marble Stairs (lm_stair_*) -> Crisp 3D shaded risers & sunlit cool-ivory treads!
    for tid in tids_for_prefix(["lm_stair_"]):
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 > H:
            continue
        im16 = out[ty:ty + 32:2, tx:tx + 32:2].copy().astype(np.int16)
        alp16 = im16[..., 3] > 200
        # Every 4 logical rows = 1 step (riser shadow at row%4==3, sunlit ivory lip at row%4==0)
        for y in range(16):
            m = alp16[y]
            if not m.any():
                continue
            if y % 4 == 3:
                im16[y, m, 0] -= 42
                im16[y, m, 1] -= 36
                im16[y, m, 2] -= 18  # cool sapphire-slate shadow riser!
            elif y % 4 == 2:
                im16[y, m, 0] -= 16
                im16[y, m, 1] -= 14
                im16[y, m, 2] -= 6
            elif y % 4 == 0:
                im16[y, m, 0] += 14
                im16[y, m, 1] += 16
                im16[y, m, 2] += 20  # crisp sunlit alabaster tread lip!
        res = np.clip(im16, 0, 255).astype(np.uint8).repeat(2, axis=0).repeat(2, axis=1)
        res[..., 3] = orig[ty:ty + 32, tx:tx + 32, 3]
        out[ty:ty + 32, tx:tx + 32] = res

    # 2. Starlit Cosmic Abyss (lm_deep0..5) -> Deep velvet cosmos indigo with crisp bright cyan/gold stars!
    for tid in tids_for_prefix(["lm_deep"]):
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 > H:
            continue
        src = orig[ty:ty + 32, tx:tx + 32]
        rgb = src[..., :3].astype(np.float32) / 255.0
        _, _, v = rgb_to_hsv(rgb)
        res = np.zeros_like(src)
        # Deep midnight sapphire cosmos background
        is_star = v > 0.28
        res[..., 0] = np.clip(rgb[..., 0] * 120 + 6, 0, 255).astype(np.uint8)
        res[..., 1] = np.clip(rgb[..., 1] * 140 + 10, 0, 255).astype(np.uint8)
        res[..., 2] = np.clip(rgb[..., 2] * 195 + 24, 0, 255).astype(np.uint8)
        # Make star motes gleam crisp & bright!
        res[is_star, 0] = np.clip(src[is_star, 0].astype(np.int32) + 36, 0, 255).astype(np.uint8)
        res[is_star, 1] = np.clip(src[is_star, 1].astype(np.int32) + 42, 0, 255).astype(np.uint8)
        res[is_star, 2] = np.clip(src[is_star, 2].astype(np.int32) + 52, 0, 255).astype(np.uint8)
        res[..., 3] = src[..., 3]
        out[ty:ty + 32, tx:tx + 32] = res

    # 3. Golden Astrolabe & Sanctum Rings (lm_sun, lm_ring, lm_core) -> Burnished N's Castle royal gold + radiant core!
    for tid in tids_for_prefix(["lm_sun", "lm_ring", "lm_core"]):
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 > H:
            continue
        src = orig[ty:ty + 32, tx:tx + 32]
        rgb = src[..., :3].astype(np.float32) / 255.0
        h, s, v = rgb_to_hsv(rgb)
        # Gold bands -> deep rich burnished metallic gold!
        is_gold = (hue_dist(h, 44.0) < 26.0) & (s > 0.22)
        # White/grey marble base behind astrolabe -> cool luminous alabaster-slate contrast!
        is_marble = (s <= 0.20) & (v > 0.45)
        h_n, s_n, v_n = h.copy(), s.copy(), v.copy()
        h_n = np.where(is_gold, np.where(v < 0.60, 31.0, 42.0), h_n)
        s_n = np.where(is_gold, np.clip(s * 1.40 + 0.10, 0.55, 0.96), s_n)
        v_n = np.where(is_gold, apply_s_curve(np.clip(v * 1.06, 0, 1), strength=0.35, pivot=0.58), v_n)
        # Marble gets sleek cool-indigo subtle tint so the warm gold astrolabe BLAZES off it!
        h_n = np.where(is_marble, 224.0, h_n)
        s_n = np.where(is_marble, np.clip(s * 0.5 + 0.11, 0.08, 0.16), s_n)
        v_n = np.where(is_marble, apply_s_curve(v * 0.92, strength=0.30, pivot=0.66), v_n)
        # Cyan core sparkles electric
        is_cyan = (hue_dist(h, 192.0) < 26.0) & (s > 0.30)
        s_n = np.where(is_cyan, np.clip(s * 1.25, 0.55, 0.98), s_n)
        v_n = np.where(is_cyan, np.clip(v * 1.14, 0.0, 1.0), v_n)
        res = np.dstack([np.clip(hsv_to_rgb(h_n, s_n, v_n) * 255.0 + 0.5, 0, 255).astype(np.uint8), src[..., 3]])
        out[ty:ty + 32, tx:tx + 32] = res

    # 4. Z_f0..3 (Spire dark deck floor) -> Crisp beveled dark indigo-gunmetal panels!
    for tid in tids_for_prefix(["Z_f"]):
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 > H:
            continue
        im16 = out[ty:ty + 32:2, tx:tx + 32:2].copy().astype(np.int16)
        im16[0, :, :3] = np.clip(im16[0, :, :3] - np.array([14, 14, 12]), 0, 255)
        im16[:, 0, :3] = np.clip(im16[:, 0, :3] - np.array([14, 14, 12]), 0, 255)
        im16[1, 1:15, :3] = np.clip(im16[1, 1:15, :3] + np.array([12, 14, 18]), 0, 255)
        im16[1:15, 1, :3] = np.clip(im16[1:15, 1, :3] + np.array([10, 12, 16]), 0, 255)
        res = np.clip(im16, 0, 255).astype(np.uint8).repeat(2, axis=0).repeat(2, axis=1)
        res[..., 3] = orig[ty:ty + 32, tx:tx + 32, 3]
        out[ty:ty + 32, tx:tx + 32] = res

    # 5. Q_f0..2 (25901, 25902, 25903) -> Complete Plasma Frigate beveled gunmetal deck plates!
    for v_idx, tid in enumerate((25901, 25902, 25903)):
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 <= H:
            deck = draw_plasma_frigate_deck_tile(variant=v_idx)
            deck[..., 3] = orig[ty:ty + 32, tx:tx + 32, 3]
            out[ty:ty + 32, tx:tx + 32] = deck

    # 6. lm_monitors (2x2: 25955..25958) -> Holographic cyan/amber tactical radar console!
    if "lm_monitors" in srjc:
        for layer in srjc["lm_monitors"]["layers"]:
            if any(t >= 384 for row in layer for t in row):
                comp64 = np.zeros((64, 64, 4), dtype=np.uint8)
                for ry in range(2):
                    for rx in range(2):
                        tid = layer[ry][rx]
                        if tid >= 384:
                            i = tid - 384
                            tx, ty = (i % 8) * 32, (i // 8) * 32
                            comp64[ry * 32:(ry + 1) * 32, rx * 32:(rx + 1) * 32] = orig[ty:ty + 32, tx:tx + 32]
                new64 = draw_plasma_holographic_monitors(comp64)
                for ry in range(2):
                    for rx in range(2):
                        tid = layer[ry][rx]
                        if tid >= 384:
                            i = tid - 384
                            tx, ty = (i % 8) * 32, (i // 8) * 32
                            out[ty:ty + 32, tx:tx + 32] = new64[ry * 32:(ry + 1) * 32, rx * 32:(rx + 1) * 32]

    # 7. Royal Crimson Velvet & Burnished Gold Carpet (lm_carpet_*)
    for tid in range(25904, 25913):
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 <= H:
            out[ty:ty + 32, tx:tx + 32] = upgrade_royal_carpet(
                orig[ty:ty + 32, tx:tx + 32], is_center=(tid == 25908)
            )


def draw_plasma_frigate_deck_tile(variant: int = 0) -> np.ndarray:
    """Replace noisy dot-matrix Q_f0..2 steel grate with sleek B2W2 Plasma Frigate beveled gunmetal deck plating!"""
    im16 = np.zeros((16, 16, 4), dtype=np.uint8)
    im16[..., 3] = 255
    for y in range(16):
        t = y / 15.0
        r = int(84 - 14 * t)
        g = int(96 - 14 * t)
        b = int(120 - 14 * t)
        im16[y, :, :3] = (r, g, b)

    seam = (35, 43, 58)
    hi = (114, 128, 152)
    sh = (52, 62, 80)
    rivet = (40, 48, 64)

    im16[0, :, :3] = seam
    im16[:, 0, :3] = seam
    im16[1, 1:15, :3] = hi
    im16[1:15, 1, :3] = hi
    im16[15, 1:, :3] = sh
    im16[1:, 15, :3] = sh

    for ry, rx in ((2, 2), (2, 13), (13, 2), (13, 13)):
        im16[ry, rx, :3] = rivet
        im16[ry + 1 if ry == 2 else ry - 1, rx, :3] = (104, 118, 140)

    if variant == 1:
        im16[5:11, 5:11, :3] = (66, 76, 96)
        im16[5, 5:11, :3] = seam
        im16[5:11, 5, :3] = seam
        im16[10, 5:11, :3] = hi
        im16[5:11, 10, :3] = hi
    elif variant == 2:
        for vy in (6, 9):
            im16[vy, 4:12, :3] = (34, 40, 54)
            im16[vy + 1, 4:12, :3] = (106, 120, 142)

    return im16.repeat(2, axis=0).repeat(2, axis=1)


def draw_plasma_holographic_monitors(orig_2x2: np.ndarray) -> np.ndarray:
    """Replace flat 4-color MS-Paint lm_monitors (2x2 tiles = 64x64) with sleek B2W2 Plasma Frigate
    dual-tier glowing holographic cyan/amber radar & waveform tactical displays, respecting exact original alpha!"""
    im32 = orig_2x2[::2, ::2].copy()
    bezel_dark = (24, 30, 44)
    bezel_mid = (50, 60, 82)
    bezel_hi = (96, 112, 138)
    scr_bg = (12, 38, 56)
    scr_grid = (20, 62, 88)
    cyan_mid = (40, 186, 224)
    cyan_hi = (146, 246, 255)
    amber_hi = (255, 200, 78)
    amber_mid = (214, 132, 34)

    # Top display panel (y=1..14, x=2..29) — fits cleanly inside top monitor row opaque alpha
    im32[1:15, 2:30, :3] = bezel_dark
    im32[2:14, 3:29, :3] = bezel_mid
    im32[2, 3:29, :3] = bezel_hi
    im32[2:14, 3, :3] = bezel_hi
    im32[4:13, 5:27, :3] = scr_bg
    for gy in (6, 9, 12):
        im32[gy, 5:27, :3] = scr_grid
    for gx in (9, 15, 21):
        im32[4:13, gx, :3] = scr_grid
    # Left radar target + right waveform on top screen
    rcx, rcy = 10, 8
    for y in range(4, 13):
        for x in range(6, 15):
            d = math.hypot(x - rcx, y - rcy)
            if 3.0 <= d <= 3.9:
                im32[y, x, :3] = cyan_mid
            elif 1.2 <= d <= 2.0:
                im32[y, x, :3] = cyan_hi
    im32[rcy, rcx, :3] = amber_hi
    im32[rcy - 2, rcx + 2, :3] = amber_hi
    wave_y = [10, 8, 6, 8, 5, 9, 7, 8, 10]
    for idx, wy in enumerate(wave_y):
        x = 17 + idx
        if x < 26:
            im32[wy, x, :3] = cyan_hi
            if wy + 1 < 12:
                im32[wy + 1, x, :3] = cyan_mid
    im32[5, 17:24, :3] = amber_hi

    # Bottom display panel (y=17..30, x=2..29) — fits cleanly inside bottom monitor row opaque alpha
    im32[17:31, 2:30, :3] = bezel_dark
    im32[18:30, 3:29, :3] = bezel_mid
    im32[18, 3:29, :3] = bezel_hi
    im32[18:30, 3, :3] = bezel_hi
    im32[20:27, 5:27, :3] = scr_bg
    for gy in (22, 25):
        im32[gy, 5:27, :3] = scr_grid
    for gx in (9, 15, 21):
        im32[20:27, gx, :3] = scr_grid
    # Tactical telemetry bars (cyan & amber readouts)
    im32[21, 6:14, :3] = cyan_hi
    im32[23, 6:11, :3] = cyan_mid
    im32[25, 6:13, :3] = amber_hi
    im32[21, 17:25, :3] = amber_hi
    im32[23, 17:23, :3] = amber_mid
    im32[25, 17:25, :3] = cyan_hi
    # Bottom LED status row
    im32[28, 5:27, :3] = (32, 40, 56)
    for lx, col in ((6, cyan_hi), (8, cyan_mid), (11, amber_hi), (14, cyan_hi), (18, cyan_hi), (21, amber_hi), (24, cyan_mid)):
        im32[28, lx, :3] = col

    res = im32.repeat(2, axis=0).repeat(2, axis=1)
    res[..., 3] = orig_2x2[..., 3]
    return res


def upgrade_royal_carpet(tile_rgba: np.ndarray, is_center: bool = False) -> np.ndarray:
    """Enrich flat maroon lm_carpet_* into rich B2W2 royal crimson velvet with burnished gold filigree."""
    rgb = tile_rgba[..., :3].astype(np.float32) / 255.0
    h, s, v = rgb_to_hsv(rgb)
    is_red = (hue_dist(h, 352.0) < 28.0) & (s > 0.25)
    is_gold = (hue_dist(h, 44.0) < 22.0) & (s > 0.30)
    h_new, s_new, v_new = h.copy(), s.copy(), v.copy()
    h_new = np.where(is_red, 350.0, h_new)
    s_new = np.where(is_red, np.clip(s * 1.25, 0.55, 0.88), s_new)
    v_new = np.where(is_red, apply_s_curve(v * 0.90, strength=0.30, pivot=0.44), v_new)

    h_new = np.where(is_gold, 42.0, h_new)
    s_new = np.where(is_gold, np.clip(s * 1.25, 0.62, 0.92), s_new)
    v_new = np.where(is_gold, np.clip(v * 1.15, 0.0, 0.98), v_new)

    out = np.clip(hsv_to_rgb(h_new, s_new, v_new) * 255.0 + 0.5, 0, 255).astype(np.uint8)
    if is_center:
        im16 = out[::2, ::2].copy().astype(np.int16)
        yy, xx = np.mgrid[0:16, 0:16]
        pat = ((xx + yy) % 8 == 0) | ((xx - yy) % 8 == 0)
        red16 = is_red[::2, ::2]
        im16[pat & red16, 0] += 14
        im16[pat & red16, 1] += 4
        im16[pat & red16, 2] += 6
        out = np.clip(im16, 0, 255).astype(np.uint8).repeat(2, axis=0).repeat(2, axis=1)
    return np.dstack([out, tile_rgba[..., 3]])


def add_cave_strata_relief(tile_rgba: np.ndarray, is_lip: bool = False, is_base: bool = False) -> np.ndarray:
    """Enhance 3D Chargestone stratified rock depth & overhang shadows on S_/L_/E_ cave wall tiles."""
    im16 = tile_rgba[::2, ::2].copy().astype(np.int16)
    alp16 = im16[..., 3] > 200
    for y in (4, 10):
        m = alp16[y]
        im16[y, m, :3] -= np.array([12, 12, 8])
        if y + 1 < 16:
            m2 = alp16[y + 1]
            im16[y + 1, m2, :3] += np.array([9, 8, 10])
    if is_lip:
        m_top = alp16[1:3]
        im16[1:3, :, :3][m_top] += np.array([16, 14, 18])
        m_bot = alp16[13:16]
        im16[13:16, :, :3][m_bot] -= np.array([18, 18, 12])
    if is_base:
        m_bot = alp16[13:16]
        im16[13:16, :, :3][m_bot] -= np.array([22, 22, 14])
    out = np.clip(im16, 0, 255).astype(np.uint8).repeat(2, axis=0).repeat(2, axis=1)
    out[..., 3] = tile_rgba[..., 3]
    return out


# ---------------------------------------------------------------------------
# MODULE 3: Silky Gen 5 B2W2 Pixel-Art Water, Shore, Waterfall & Ground Autotiles
# ---------------------------------------------------------------------------
# Curated calm velvety B2W2 water palettes:
# (bank_undercut, deep_velvet, mid_velvet, soft_swell, wave_glint, shallow_shelf, shoreline_foam)
WATER_PALETTES = {
    "salt_lake": (
        (90, 66, 88),      # #5A4258 plum-salt undercut grounding the rose-salt lip
        (12, 79, 90),      # #0C4F5A deep brine
        (23, 119, 126),    # #17777E mid brine
        (42, 154, 154),    # #2A9A9A brine-mint swell
        (108, 200, 192),   # #6CC8C0 specular brine glint
        (72, 178, 174),    # #48B2AE luminous brine shelf
        (230, 251, 246),   # #E6FBF6 crisp salt foam
    ),
    "ocean": (
        (14, 58, 118),
        (24, 96, 166),
        (30, 112, 182),
        (44, 134, 202),
        (96, 182, 234),
        (64, 160, 220),
        (228, 248, 255),
    ),
    "sea_deep": (
        (10, 38, 86),
        (16, 62, 122),
        (22, 76, 140),
        (32, 96, 162),
        (66, 136, 196),
        (42, 112, 176),
        (210, 240, 255),
    ),
    "river_grass": (
        (16, 66, 126),
        (28, 106, 176),
        (36, 124, 192),
        (52, 148, 212),
        (112, 196, 240),
        (74, 172, 226),
        (226, 248, 255),
    ),
    "frozen_water": (
        (18, 52, 98),
        (32, 86, 142),
        (42, 104, 162),
        (58, 128, 184),
        (118, 184, 226),
        (82, 154, 206),
        (232, 248, 255),
    ),
    "frozen_ice": (
        (110, 154, 198),
        (150, 192, 228),
        (168, 208, 238),
        (192, 226, 248),
        (236, 250, 255),
        (212, 238, 252),
        (248, 254, 255),
    ),
    "cave_water": (
        (10, 36, 56),
        (18, 62, 88),
        (24, 78, 104),
        (34, 98, 124),
        (72, 146, 166),
        (46, 118, 140),
        (198, 238, 244),
    ),
    "magma": (
        (96, 16, 10),
        (178, 46, 14),
        (214, 74, 16),
        (242, 116, 22),
        (255, 192, 56),
        (248, 142, 28),
        (255, 236, 142),
    ),
}


def synthesize_water_autotile(arr: np.ndarray, pal_key: str, bank_mode: str, is_ice_sheet: bool = False) -> np.ndarray:
    """Transform RMXP water autotiles into silky, calm Gen 5 B2W2 bathymetry with
    delicate staggered pixel-art wave glints (ZERO zebra stripes, ZERO waffle grid!)
    and crisp organic shoreline foam wrapping every corner seamlessly."""
    H, W = arr.shape[:2]
    n_frames = max(1, W // 96)
    out = arr.copy()
    c_under, c_deep, c_mid, c_swell, c_glint, c_shallow, c_foam = [
        np.array(c, dtype=np.uint8) for c in WATER_PALETTES[pal_key]
    ]

    for fi in range(n_frames):
        fx0 = fi * 96
        frame = arr[:, fx0:fx0 + 96].copy()
        alp = frame[..., 3]

        # Preserve unused pure-white RMXP slot [0:32, 32:64] untouched!
        r0, g0, b0 = frame[..., 0], frame[..., 1], frame[..., 2]
        pure_white_slot = np.zeros((H, 96), dtype=bool)
        slot_box = (r0[:32, 32:64] > 248) & (g0[:32, 32:64] > 248) & (b0[:32, 32:64] > 248)
        if slot_box.mean() > 0.85:
            pure_white_slot[:32, 32:64] = True

        # 1. Recolor shore/bank pixels with exact matching ground biome shader
        if bank_mode == "nature":
            bank_rgb = shade_outdoor_nature(frame[..., :3], alp, warm_timber=False)
        elif bank_mode == "snow":
            bank_rgb = shade_snow_biome(frame[..., :3], alp)
        elif bank_mode == "salt_cave":
            # Pale rose-salt crust ring: keeps Brinecut's salt identity and creates crisp
            # figure-ground separation against both slate-violet cave floor and brine water.
            bh, bs, bv = rgb_to_hsv(frame[..., :3].astype(np.float32) / 255.0)
            bank_rgb = shade_cave_strata(frame[..., :3], alp, mode="salt")
            # Map original bank tones (shadow ~0.58, mid ~0.77, bright lip ~0.87..0.98)
            # to rose-salt crust (#A8879B -> #D6BAC8 -> #F0E2E8)
            is_crust = (alp > 128) & (bv > 0.52)
            t_hi = smoothstep(0.76, 0.94, bv)
            t_mid = smoothstep(0.54, 0.78, bv)
            c_sh = np.array([168.0, 135.0, 155.0], dtype=np.float32)   # #A8879B crust shadow
            c_md = np.array([214.0, 186.0, 200.0], dtype=np.float32)   # #D6BAC8 rose-salt crust
            c_hi = np.array([240.0, 226.0, 232.0], dtype=np.float32)   # #F0E2E8 bright salt lip
            crust = c_sh * (1.0 - t_mid[..., None]) + c_md * t_mid[..., None]
            crust = crust * (1.0 - t_hi[..., None]) + c_hi * t_hi[..., None]
            bank_rgb = np.where(is_crust[..., None], np.clip(crust + 0.5, 0, 255).astype(np.uint8), bank_rgb)
        elif bank_mode == "limestone_cave":
            bank_rgb = shade_cave_strata(frame[..., :3], alp, mode="limestone")
        elif bank_mode == "volcanic":
            bank_rgb = shade_cave_strata(frame[..., :3], alp, mode="volcanic")
        else:
            bank_rgb = shade_outdoor_nature(frame[..., :3], alp, warm_timber=False)

        # 2. Identify water pixels on 48x64 logical grid
        f16_rgb = frame[::2, ::2, :3].astype(np.float32) / 255.0
        f16_a = (frame[::2, ::2, 3] > 128) & (~pure_white_slot[::2, ::2])
        h16, s16, v16 = rgb_to_hsv(f16_rgb)

        if pal_key == "magma":
            wmask = f16_a & (hue_dist(h16, 26.0) < 28.0) & (s16 > 0.55) & (v16 > 0.45)
        elif is_ice_sheet:
            wmask = f16_a & (hue_dist(h16, 206.0) < 30.0) & (v16 > 0.72)
            rim = f16_a & (v16 < 0.74)
            wmask = wmask & (~ndimage.binary_dilation(rim, iterations=1))
        elif pal_key == "salt_lake":
            wmask = f16_a & (hue_dist(h16, 174.0) < 26.0) & (s16 > 0.16) & (v16 > 0.58)
        elif pal_key in ("ocean", "sea_deep"):
            wmask = f16_a & (hue_dist(h16, 215.0) < 42.0) & (s16 > 0.25)
        elif pal_key == "frozen_water":
            wmask = f16_a & (hue_dist(h16, 215.0) < 34.0) & (s16 > 0.18) & (v16 > 0.34) & (v16 < 0.86)
        elif pal_key == "cave_water":
            wmask = f16_a & (hue_dist(h16, 198.0) < 35.0) & (s16 > 0.28) & (v16 > 0.22)
        else:
            wmask = f16_a & (hue_dist(h16, 212.0) < 34.0) & (s16 > 0.28) & (v16 > 0.32)

        wmask = ndimage.binary_opening(wmask, structure=np.ones((2, 2))) | (wmask & ndimage.binary_erosion(wmask))
        if wmask[34:46, 18:30].mean() > 0.7:
            wmask[32:48, 16:32] = True

        # 3. Distance transform from shoreline bank (ignoring unused white slot)
        bank_mask = f16_a & (~wmask)
        if bank_mask.any():
            dist = ndimage.distance_transform_edt(~bank_mask)
        else:
            dist = np.full(wmask.shape, 20.0, dtype=np.float32)

        # 4. Synthesize silky calm period-16 B2W2 open water + sparse staggered horizontal pixel glints!
        ly, lx = np.mgrid[0:64, 0:48].astype(np.float32)
        phase = 2.0 * math.pi * (fi / float(n_frames))
        kx = 2.0 * math.pi * lx / 16.0
        ky = 2.0 * math.pi * ly / 16.0

        water16 = np.zeros((64, 48, 3), dtype=np.uint8)

        if is_ice_sheet:
            # Crisp diagonal glacier reflection bands over smooth ice blue
            water16[:, :] = c_mid
            d_mod = (lx + ly) % 16.0
            water16[(d_mod >= 2) & (d_mod < 5)] = c_swell
            water16[(d_mod >= 3) & (d_mod < 4)] = c_glint
            water16[(d_mod >= 10) & (d_mod < 12)] = c_swell
            water16[(d_mod >= 14) & (d_mod < 16)] = c_deep
        elif pal_key == "magma":
            # Smooth undulating glowing lava currents (no checkerboard!)
            flow = np.sin(ky + 0.55 * np.sin(kx + phase) - phase) * 0.55 + np.cos(kx + ky * 0.5 + phase) * 0.35
            water16[:, :] = c_mid
            water16[flow < -0.35] = c_deep
            water16[flow > 0.25] = c_swell
            water16[flow > 0.65] = c_glint
            if bank_mask.any():
                water16[wmask & (dist <= 1.6)] = c_under
        else:
            # CALM SILKY B2W2 BASE: ~75% velvety mid/deep water with subtle low-contrast diagonal swell!
            # Exact period 16 in BOTH x and y -> 100.00% seamless across unlimited ocean/lagoon tiles!
            swell = (
                0.55 * np.sin(ky + 0.35 * np.sin(kx + phase) - phase)
                + 0.45 * np.cos(kx - ky * 0.0 + 0.5 * phase) * 0.55
            )
            water16[:, :] = c_mid
            water16[swell < -0.22] = c_deep
            water16[swell > 0.42] = c_swell

            # SPARSE STAGGERED SHORT B2W2 PIXEL-ART WAVE GLINTS (authentic DS Unova water!)
            # Hand-placed 16x16 seamless motif of 3 short broken curved wave ripples (length 3-5px)
            # drifting smoothly right/left across animation frames!
            drift_x = int(round((fi / float(n_frames)) * 16)) % 16
            sx = (lx.astype(np.int32) - drift_x) % 16
            sy = ly.astype(np.int32) % 16
            # Ripple 1 (y=3, x=2..5), Ripple 2 (y=9, x=9..13), Ripple 3 (y=14, x=5..7)
            r1_soft = ((sy == 3) & (sx >= 1) & (sx <= 6)) | ((sy == 4) & (sx >= 3) & (sx <= 5))
            r2_soft = ((sy == 9) & (sx >= 8) & (sx <= 13)) | ((sy == 10) & (sx >= 10) & (sx <= 12))
            r3_soft = (sy == 14) & (sx >= 4) & (sx <= 8)
            water16[r1_soft | r2_soft | r3_soft] = c_swell

            # Crisp 2-3px bright specular glints inside the wave crests
            g1 = (sy == 3) & (sx >= 2) & (sx <= 4)
            g2 = (sy == 9) & (sx >= 10) & (sx <= 12)
            g3 = (sy == 14) & (sx >= 5) & (sx <= 6)
            water16[g1 | g2 | g3] = c_glint

            # Soft luminous bathymetric shallow shelf near shorelines (dist 2.2..5.5)
            if bank_mask.any():
                shallow = wmask & (dist > 2.2) & (dist <= 5.2)
                water16[shallow & (swell > -0.15)] = c_shallow
                # Immediate 1px dark bank undercut shadow (grounds banks into water!)
                undercut = wmask & (dist <= 1.25)
                water16[undercut] = c_under
                # Crisp organic frothy B2W2 white shoreline foam ripple!
                foam_wave = np.sin(kx * 2.0 + ky * 2.0 + phase)
                if pal_key == "salt_lake":
                    # Luminous turquoise glow + crisp white foam ring around Brinecut crystal islets!
                    glow_band = wmask & (dist > 2.2) & (dist <= 6.2)
                    water16[glow_band & (water16[..., 1] < c_shallow[1])] = c_shallow
                    foam_ring = wmask & (dist > 1.05) & (dist <= (2.35 + 0.30 * foam_wave))
                    foam2 = wmask & (dist > 3.4) & (dist <= 4.2) & (foam_wave > 0.45)
                    water16[foam2] = c_glint
                else:
                    foam_ring = wmask & (dist > 1.15) & (dist <= (2.10 + 0.25 * foam_wave))
                water16[foam_ring] = c_foam

        water32 = water16.repeat(2, axis=0).repeat(2, axis=1)
        wmask32 = wmask.repeat(2, axis=0).repeat(2, axis=1)
        res_rgb = np.where(wmask32[..., None], water32, bank_rgb)
        if pure_white_slot.any():
            res_rgb[pure_white_slot] = frame[pure_white_slot, :3]
        out[:, fx0:fx0 + 96, :3] = res_rgb
        out[:, fx0:fx0 + 96, 3] = alp

    return out


def synthesize_waterfall_autotile(arr: np.ndarray, kind: str) -> np.ndarray:
    """Crisp 4-frame animated B2W2 cascading waterfall (128x32), preserving exact dimensions & alpha."""
    H, W = arr.shape[:2]
    n_frames = max(1, W // 32)
    out = arr.copy()
    deep = (26, 98, 174)
    mid = (48, 148, 218)
    bright = (104, 198, 246)
    foam = (198, 240, 255)
    white = (244, 252, 255)

    for fi in range(n_frames):
        fx0 = fi * 32
        f16 = np.zeros((16, 16, 3), dtype=np.uint8)
        shift = fi * 4
        if kind == "body":
            for y in range(16):
                ys = (y - shift) % 16
                for x in range(16):
                    if x in (0, 15):
                        c = deep
                    elif x in (1, 14):
                        c = mid if (ys % 4 != 0) else bright
                    else:
                        v = (
                            math.sin(2.0 * math.pi * x / 5.0) * 0.45
                            + math.sin(2.0 * math.pi * (ys + (x % 3) * 3) / 16.0) * 0.55
                        )
                        if v > 0.62:
                            c = white
                        elif v > 0.28:
                            c = foam
                        elif v > -0.15:
                            c = bright
                        elif v > -0.55:
                            c = mid
                        else:
                            c = deep
                    f16[y, x] = c
        elif kind == "crest":
            for y in range(16):
                for x in range(16):
                    bump = int(round(math.sin(2.0 * math.pi * (x + fi * 2) / 8.0)))
                    if y < 4:
                        c = deep if (x + fi) % 3 == 0 else mid
                    elif y < 7 + bump:
                        c = bright
                    elif y < 11 + bump:
                        c = white if (x + y + fi) % 3 != 0 else foam
                    else:
                        c = foam if (x + fi) % 2 == 0 else bright
                    f16[y, x] = c
        else:
            for y in range(16):
                for x in range(16):
                    b1 = math.sin(2.0 * math.pi * (x + fi * 2) / 16.0) * 1.5
                    b2 = math.cos(2.0 * math.pi * (x * 2 - fi * 3) / 16.0) * 1.0
                    cy_lo = 11.5 + b1 * 0.6 + b2 * 0.5
                    if y < 3:
                        c = bright if (x + fi) % 2 == 0 else foam
                    elif y < 9 + b2 * 0.7:
                        c = white if (x + y + fi) % 4 != 0 else foam
                    elif y < cy_lo:
                        c = foam if (x + fi) % 2 == 0 else bright
                    else:
                        c = mid if (x + fi) % 3 == 0 else deep
                    f16[y, x] = c

        block = f16.repeat(2, axis=0).repeat(2, axis=1)
        out[:, fx0:fx0 + 32, :3] = block
        out[:, fx0:fx0 + 32, 3] = arr[:, fx0:fx0 + 32, 3]
    return out


def reskin_autotile(name: str, im: Image.Image) -> Image.Image:
    """Dispatch each RMXP autotile to its exact B2W2 shader/synthesizer, preserving dimensions & alpha."""
    arr = np.asarray(im.convert("RGBA")).copy()
    alp = arr[..., 3]

    if name == "RJ Waterfall":
        res = synthesize_waterfall_autotile(arr, "body")
    elif name == "RJ Waterfall bottom":
        res = synthesize_waterfall_autotile(arr, "bottom")
    elif name == "RJ Waterfall crest":
        res = synthesize_waterfall_autotile(arr, "crest")
    elif name == "PF Salt Lake":
        res = synthesize_water_autotile(arr, "salt_lake", "salt_cave")
    elif name in ("RJ Ocean", "RJ Sea", "RJ Hoenn Sea"):
        res = synthesize_water_autotile(arr, "ocean", "nature")
    elif name == "RJ Sea deep":
        res = synthesize_water_autotile(arr, "sea_deep", "nature")
    elif name in ("RJ Sea(Grass)", "water2", "RJ Still water"):
        res = synthesize_water_autotile(arr, "river_grass", "nature")
    elif name in ("RJ Sand shore", "RJ Sand shore_2"):
        res = synthesize_water_autotile(arr, "ocean", "nature")
    elif name in ("RB Still water snow", "RJ KristilineWatersFrozen"):
        res = synthesize_water_autotile(arr, "frozen_water", "snow")
    elif name == "PF Frozen Pond":
        res = synthesize_water_autotile(arr, "frozen_ice", "snow", is_ice_sheet=True)
    elif name in ("PF Lock Water", "PF Sea Cave", "PF Cave Pool"):
        res = synthesize_water_autotile(arr, "cave_water", "limestone_cave")
    elif name in ("PF Magma", "Lava", "Lavafall"):
        res = synthesize_water_autotile(arr, "magma", "volcanic")
    elif name == "RJ KristilineDirt":
        # Cool dark winter slate-earth (instead of reddish-plum!)
        res = arr.copy()
        rgb = arr[..., :3].astype(np.float32) / 255.0
        h, s, v = rgb_to_hsv(rgb)
        h_n = lerp_hue(h, 224.0, 0.72)
        s_n = np.clip(s * 0.55 + 0.14, 0.12, 0.26)
        v_n = apply_s_curve(v * 0.84, strength=0.25, pivot=0.44)
        res[..., :3] = np.clip(hsv_to_rgb(h_n, s_n, v_n) * 255.0 + 0.5, 0, 255).astype(np.uint8)
    elif name in ("PF Packed Snow", "Bleed grass", "Bleed water"):
        res = arr.copy()
        res[..., :3] = shade_snow_biome(arr[..., :3], alp)
    else:
        # Dirt, DirtDark, Saltmere Cobbles, Saltmere Flags, Gravel Spring, Gravel(G), Tall Grass Flowers 2:
        # EXACT SAME outdoor nature shader so grass fringes are 100.00% bit-exact!
        res = arr.copy()
        res[..., :3] = shade_outdoor_nature(arr[..., :3], alp, warm_timber=False)
        if name in ("PF Saltmere Cobbles", "PF Saltmere Flags", "RJ Dirt", "RJ DirtDark"):
            orig_rgb = arr[..., :3].astype(np.float32) / 255.0
            oh, os_, ov = rgb_to_hsv(orig_rgb)
            is_grass = (hue_dist(oh, 152.0) < 26.0) & (os_ > 0.16) & (ov > 0.45)
            interior = (~is_grass) & (alp > 128)
            rgb_cur = res[..., :3].astype(np.float32) / 255.0
            ch, cs, cv = rgb_to_hsv(rgb_cur)
            if name == "PF Saltmere Flags":
                # Crisp weathered maritime limestone flagstones with cool slate mortar!
                is_mortar = cv < 0.52
                ch = np.where(is_mortar, lerp_hue(ch, 220.0, 0.45), ch)
                cs = np.where(is_mortar, np.clip(cs * 0.65, 0.08, 0.22), np.clip(cs * 0.92, 0.14, 0.34))
                cv_e = apply_s_curve(cv * 0.91, strength=0.34, pivot=0.56)
            else:
                cv_e = apply_s_curve(cv * 0.96, strength=0.20, pivot=0.46)
            polished = np.clip(hsv_to_rgb(ch, cs, cv_e) * 255.0 + 0.5, 0, 255).astype(np.uint8)
            res[..., :3] = np.where(interior[..., None], polished, res[..., :3])

    res[..., 3] = alp
    return Image.fromarray(res, mode="RGBA")


# ---------------------------------------------------------------------------
# MODULE 4: PF Rejuv.png Biome-Aware Semantic Tileset Remaster
# ---------------------------------------------------------------------------
def build_pf_rejuv_tile_taxonomy():
    """Map every tile ID in PF Rejuv.png (384..28943) to its exact semantic biome class."""
    comp = json.load(open(REPO / "mapgen/data/rj_compose.json"))["parts"]
    srjc = json.load(open(REPO / "mapgen/data/stamps_rjc.json"))
    srj = json.load(open(REPO / "mapgen/data/stamps_rj.json"))
    rjc = json.load(open(REPO / "mapgen/data/rj_custom.json"))

    tags = {}
    pf_offset = comp["pf"]["offset"]

    for _, rel_idx in rjc.get("snow", {}).items():
        if isinstance(rel_idx, int):
            tags[pf_offset + rel_idx] = "snow"

    prefix_biome = {
        "S": "cave_salt", "Sl": "cave_salt",
        "salt0": "cave_salt", "salt1": "cave_salt", "salt2": "cave_salt", "salt3": "cave_salt",
        "gs": "cave_salt", "cv": "cave_salt",
        "L": "cave_limestone", "Ll": "cave_limestone", "T": "cave_limestone",
        "E": "cave_volcanic", "El": "cave_volcanic",
        "lm": "lumen", "lb": "lumen", "lmw": "lumen",
        "Q": "lumen", "Z": "lumen", "Y": "lumen",
        "F": "lumen", "H": "lumen", "N": "lumen", "P": "lumen", "G": "lumen", "A": "lumen", "B": "lumen",
        "ch": "snow_chalet", "sn": "snow", "bl": "snow", "cr": "snow", "gw": "snow",
        "wb": "timber", "th": "timber", "wh": "timber", "sp": "timber",
        "hb": "timber", "gt": "timber", "fw": "timber", "wr": "timber", "eb": "timber", "mr": "timber",
        "mn": "interior",
        "pf": "nature", "gd": "nature",
        "gp00": "nature", "gp01": "nature", "gp10": "nature", "gp11": "nature",
        "gr": "nature", "gdc": "nature", "sdc": "nature", "gdl": "nature", "sdl": "nature",
        "lg": "nature", "lgc": "nature", "lgd": "nature", "lgs": "nature",
        "cs": "nature", "qy": "nature", "rw": "nature", "nr": "nature",
        "ck": "nature", "dk": "nature", "sk": "nature",
        "brine": "nature", "brp": "nature", "brg": "nature", "brx": "nature",
        "dye": "nature", "dl": "nature", "df": "nature",
        "sb": "nature", "bw": "nature", "st": "nature", "tb": "nature",
    }

    for k, st in srjc.items():
        pref = k.split("_")[0]
        biome = prefix_biome.get(pref)
        if not biome:
            continue
        for layer in st.get("layers", []):
            for row in layer:
                for tid in row:
                    if tid >= pf_offset:
                        tags[tid] = biome

    for k, st in srj.items():
        if k.startswith(("gl_", "sh_")) and not k.endswith("_emblem"):
            for layer in st.get("layers", []):
                for row in layer:
                    for tid in row:
                        if tid >= 384:
                            tags[tid] = "timber"

    return comp, srjc, srj, tags


def reskin_pf_rejuv(im: Image.Image) -> Image.Image:
    orig = np.asarray(im.convert("RGBA")).copy()
    out = orig.copy()
    comp, srjc, srj, tags = build_pf_rejuv_tile_taxonomy()

    # Step 1: Fast vectorized row-band base shaders for Rejuv/Reborn base parts
    part_modes = {
        "gl": "nature_timber",
        "sh": "nature",
        "ak": "nature",
        "kf": "snow",
        "rb4": "nature",
        "ap": "nature",
        "pf": "nature",
    }
    for pname, pinfo in comp.items():
        r0 = ((pinfo["offset"] - 384) // 8) * 32
        r1 = min(orig.shape[0], r0 + (pinfo["tiles"] // 8) * 32)
        sub = orig[r0:r1]
        mode = part_modes[pname]
        if mode == "snow":
            out[r0:r1, :, :3] = shade_snow_biome(sub[..., :3], sub[..., 3])
        elif mode == "nature_timber":
            out[r0:r1, :, :3] = shade_outdoor_nature(sub[..., :3], sub[..., 3], warm_timber=True)
        else:
            out[r0:r1, :, :3] = shade_outdoor_nature(sub[..., :3], sub[..., 3], warm_timber=False)

    # Step 2: Semantic per-tile-ID specialized biome shaders (batched by biome for speed!)
    by_biome = {}
    for tid, biome in tags.items():
        # Skip tiles whose part already got the identical shader!
        if biome == "nature" and tid < comp["pf"]["offset"] and not (comp["kf"]["offset"] <= tid < comp["rb4"]["offset"]):
            continue
        by_biome.setdefault(biome, []).append(tid)

    for biome, tids in by_biome.items():
        valid = [t for t in tids if ((t - 384) // 8) * 32 + 32 <= orig.shape[0]]
        if not valid:
            continue
        # Stack all tiles of this biome into (N, 32, 32, 4) -> single blazing-fast vectorized numpy call!
        coords = [(((t - 384) % 8) * 32, ((t - 384) // 8) * 32) for t in valid]
        batch = np.stack([orig[ty:ty + 32, tx:tx + 32] for tx, ty in coords], axis=0)
        if biome == "cave_salt":
            res_rgb = shade_cave_strata(batch[..., :3], batch[..., 3], mode="salt")
        elif biome == "cave_limestone":
            res_rgb = shade_cave_strata(batch[..., :3], batch[..., 3], mode="limestone")
        elif biome == "cave_volcanic":
            res_rgb = shade_cave_strata(batch[..., :3], batch[..., 3], mode="volcanic")
        elif biome == "lumen":
            res_rgb = shade_lumen_metropolis(batch[..., :3], batch[..., 3])
        elif biome == "snow":
            res_rgb = shade_snow_biome(batch[..., :3], batch[..., 3])
        elif biome == "snow_chalet":
            rgb_s = shade_snow_biome(batch[..., :3], batch[..., 3])
            oh, os_, ov = rgb_to_hsv(batch[..., :3].astype(np.float32) / 255.0)
            is_wood = (hue_dist(oh, 28.0) < 24.0) & (os_ > 0.16) & (ov < 0.72)
            rgb_w = shade_outdoor_nature(batch[..., :3], batch[..., 3], warm_timber=True)
            res_rgb = np.where(is_wood[..., None], rgb_w, rgb_s)
        elif biome == "timber":
            res_rgb = shade_outdoor_nature(batch[..., :3], batch[..., 3], warm_timber=True)
        elif biome == "interior":
            res_rgb = shade_interior_b2w2(batch[..., :3], batch[..., 3], variant="wood")
        else:
            res_rgb = shade_outdoor_nature(batch[..., :3], batch[..., 3], warm_timber=False)

        for idx, (tx, ty) in enumerate(coords):
            out[ty:ty + 32, tx:tx + 32, :3] = res_rgb[idx]

    # Step 3: Fast seamless 16x16-logical B2W2 grass-blade micro-texture on flat uniform mint-grass tiles
    grass_tids = list(range(comp["gl"]["offset"], comp["ak"]["offset"] + comp["ak"]["tiles"]))
    for k, st in srjc.items():
        if k.startswith(("gp00_", "gp01_", "gp10_", "gp11_", "gr_", "gd_g")):
            for layer in st.get("layers", []):
                for row in layer:
                    for tid in row:
                        if tid >= 384:
                            grass_tids.append(tid)
    add_seamless_grass_microtexture_fast(out, orig, grass_tids)

    # Step 4: Cave 3D stratified rock relief & overhang shadows on S_/L_/E_ walls
    cave_wall_done = set()
    for k, st in srjc.items():
        if not k.startswith(("S_", "L_", "E_")):
            continue
        is_lip = "lip" in k
        is_base = "base" in k
        is_face = "face" in k
        if not (is_lip or is_base or is_face):
            continue
        for layer in st.get("layers", []):
            for row in layer:
                for tid in row:
                    if tid >= 384 and tid not in cave_wall_done:
                        cave_wall_done.add(tid)
                        i = tid - 384
                        tx, ty = (i % 8) * 32, (i // 8) * 32
                        if ty + 32 <= out.shape[0]:
                            out[ty:ty + 32, tx:tx + 32] = add_cave_strata_relief(
                                out[ty:ty + 32, tx:tx + 32], is_lip=is_lip, is_base=is_base
                            )

    # Step 5: Warm Glowing Amber Interior Windows on ALL 69+ gl/sh Timber Lodges (incl. Briarwick Poké Center!)
    light_gl_sh_lodge_windows(out, orig, comp["gl"]["offset"], comp["sh"]["offset"] + comp["sh"]["tiles"])

    # Step 6: Lumen City Smooth Beveled Granite Paving (lm_pave0..7, lm_plaza0..1)
    pave_tids = set()
    for k, st in srjc.items():
        if k.startswith(("lm_pave", "lm_plaza")):
            for layer in st.get("layers", []):
                for row in layer:
                    for tid in row:
                        if tid >= 384:
                            pave_tids.add(tid)
    for tid in pave_tids:
        i = tid - 384
        tx, ty = (i % 8) * 32, (i // 8) * 32
        if ty + 32 <= out.shape[0]:
            out[ty:ty + 32, tx:tx + 32] = upgrade_lumen_paving_bevel(out[ty:ty + 32, tx:tx + 32], tid)

    # Step 7: HERO UPGRADE — Lumen Poké Center Ribbed Blue-Glass Conservatory Dome (lb_pc)
    if "lb_pc" in srjc:
        upgrade_lumen_conservatory_dome(out, orig, srjc["lb_pc"])

    # Step 8: HERO UPGRADES — Meridian Spire & Plate Vault (stairs, astrolabe, cosmos, Z_f, Q_f, monitors, carpet)
    upgrade_spire_sanctum_hero_tiles(out, orig, srjc)

    out[..., 3] = orig[..., 3]
    return Image.fromarray(out, mode="RGBA")


def reskin_other_tileset(name: str, im: Image.Image) -> Image.Image:
    """Remaster the remaining 7 active Prismfall physical tilesets with exact alpha & placeholder protection."""
    orig = np.asarray(im.convert("RGBA")).copy()
    out = orig.copy()
    rx_mask = red_x_placeholder_mask(orig) if name in STOCK_SHEETS_WITH_RED_X else None

    if name == "Prismfall Interior":
        out[..., :3] = shade_interior_b2w2(orig[..., :3], orig[..., 3], variant="wood")
    elif name == "PF Rejuv Halls":
        out[..., :3] = shade_interior_b2w2(orig[..., :3], orig[..., 3], variant="wood")
    elif name == "Poke Centre interior":
        out[..., :3] = shade_interior_b2w2(orig[..., :3], orig[..., 3], variant="pokecentre")
    elif name == "Mart interior":
        out[..., :3] = shade_interior_b2w2(orig[..., :3], orig[..., 3], variant="mart")
    elif name == "Interior general":
        out[..., :3] = shade_interior_b2w2(orig[..., :3], orig[..., 3], variant="wood")
    elif name == "Gyms interior":
        out[..., :3] = shade_interior_b2w2(orig[..., :3], orig[..., 3], variant="wood")
    elif name == "Prismfall City":
        out[..., :3] = shade_outdoor_nature(orig[..., :3], orig[..., 3], warm_timber=True)
        n_tiles = (orig.shape[0] // 32) * 8
        add_seamless_grass_microtexture_fast(out, orig, list(range(384, 384 + n_tiles)))

    if rx_mask is not None and rx_mask.any():
        out[rx_mask] = orig[rx_mask]
    out[..., 3] = orig[..., 3]
    return Image.fromarray(out, mode="RGBA")


# ---------------------------------------------------------------------------
# CLI Driver, Dual-Sync Writer & Verification Gate
# ---------------------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_source(sub: str, name: str, search_roots: list[Path]) -> Path | None:
    for root in search_roots:
        p = root / sub / f"{name}.png"
        if p.exists():
            return p
    return None


def main():
    t0 = time.time()
    ap = argparse.ArgumentParser(description="Prismfall Gen 3 -> True Gen 5 B2W2 Tileset & Autotile Remaster Engine")
    ap.add_argument(
        "--src-roots",
        nargs="+",
        default=[
            str(REPO / "maps_out/Graphics"),
            "/home/antigravity/pf_engine_run/game/Graphics",
        ],
        help="Ordered source directories containing pristine Tilesets/ and Autotiles/",
    )
    ap.add_argument(
        "--out-dirs",
        nargs="+",
        default=[str(REPO / "graphics"), str(REPO / "art/out/Graphics")],
        help="Destination Graphics roots (will be written byte-identically)",
    )
    ap.add_argument("--verify", action="store_true", help="Verify exact dimensions, alpha masks, and dual-sync SHA-256")
    ap.add_argument("--only", nargs="*", default=None, help="Optional subset of sheet/autotile basenames to process")
    args = ap.parse_args()

    src_roots = [Path(p) for p in args.src_roots]
    out_dirs = [Path(p) for p in args.out_dirs]
    for od in out_dirs:
        (od / "Tilesets").mkdir(parents=True, exist_ok=True)
        (od / "Autotiles").mkdir(parents=True, exist_ok=True)

    only_set = set(args.only) if args.only else None
    manifest = {"tilesets": {}, "autotiles": {}}

    for name in TILESETS_8:
        if only_set and name not in only_set:
            continue
        src_p = find_source("Tilesets", name, src_roots)
        if src_p is None:
            raise FileNotFoundError(f"Missing source tileset: {name}.png in {src_roots}")
        im = Image.open(src_p)
        orig_size = im.size
        orig_alpha = np.asarray(im.convert("RGBA"))[..., 3]

        ts0 = time.time()
        print(f"[Tileset] Reskinning {name}.png {orig_size} ...", end=" ", flush=True)
        upgraded = reskin_pf_rejuv(im) if name == "PF Rejuv" else reskin_other_tileset(name, im)
        print(f"({time.time() - ts0:.1f}s)", flush=True)

        if args.verify:
            assert upgraded.size == orig_size, f"Size mismatch on {name}: {upgraded.size} != {orig_size}"
            assert np.array_equal(np.asarray(upgraded)[..., 3], orig_alpha), f"Alpha mask drift on {name}!"

        primary = out_dirs[0] / "Tilesets" / f"{name}.png"
        upgraded.save(primary, optimize=False)
        raw_bytes = primary.read_bytes()
        digest = hashlib.sha256(raw_bytes).hexdigest()
        for od in out_dirs[1:]:
            (od / "Tilesets" / f"{name}.png").write_bytes(raw_bytes)
        manifest["tilesets"][name] = {"size": list(orig_size), "sha256": digest, "bytes": len(raw_bytes)}

    for name in AUTOTILES_ALL:
        if only_set and name not in only_set:
            continue
        src_p = find_source("Autotiles", name, src_roots)
        if src_p is None:
            continue
        im = Image.open(src_p)
        orig_size = im.size
        orig_alpha = np.asarray(im.convert("RGBA"))[..., 3]
        upgraded = reskin_autotile(name, im)

        if args.verify:
            assert upgraded.size == orig_size, f"Size mismatch on autotile {name}: {upgraded.size} != {orig_size}"
            assert np.array_equal(np.asarray(upgraded)[..., 3], orig_alpha), f"Alpha mask drift on autotile {name}!"

        primary = out_dirs[0] / "Autotiles" / f"{name}.png"
        upgraded.save(primary, optimize=False)
        raw_bytes = primary.read_bytes()
        digest = hashlib.sha256(raw_bytes).hexdigest()
        for od in out_dirs[1:]:
            (od / "Autotiles" / f"{name}.png").write_bytes(raw_bytes)
        manifest["autotiles"][name] = {"size": list(orig_size), "sha256": digest, "bytes": len(raw_bytes)}

    if args.verify and len(out_dirs) > 1:
        for sub, items in (("Tilesets", manifest["tilesets"]), ("Autotiles", manifest["autotiles"])):
            for name, info in items.items():
                for od in out_dirs:
                    p = od / sub / f"{name}.png"
                    assert sha256_file(p) == info["sha256"], f"Dual-sync SHA mismatch on {p}"
        print(
            f"[VERIFY OK] {len(manifest['tilesets'])} tilesets + {len(manifest['autotiles'])} autotiles in {time.time() - t0:.1f}s: "
            f"100% exact sizes, 100% exact alpha masks, 100% byte-identical SHA-256 across {len(out_dirs)} roots!"
        )


if __name__ == "__main__":
    main()
