# -*- coding: utf-8 -*-
"""Draws Velmora twice from tools/worldmap/world_data.py + world_geo.py:
  art/previews/world_map.png                      painted parchment region map for the design docs (2480 x 1900)
  graphics/UI/Town Map/prismfall_velmora.png      the in-game Town Map (480 x 320, 30 x 20 squares of 16 px)
Run: python3 -I tools/worldmap/gen_world_map.py [--town-only] [--big-only]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import world_data as W   # noqa: E402
import world_geo as G    # noqa: E402

FONT_DIR = '/usr/share/fonts/truetype'
F_SERIF = FONT_DIR + '/crosextra/Caladea-Regular.ttf'
F_SERIF_B = FONT_DIR + '/crosextra/Caladea-Bold.ttf'
F_SERIF_I = FONT_DIR + '/crosextra/Caladea-Italic.ttf'
F_SERIF_BI = FONT_DIR + '/crosextra/Caladea-BoldItalic.ttf'
F_TITLE = FONT_DIR + '/baskerville/GFSBaskerville.otf'
F_CAPS = '/usr/share/texmf/fonts/opentype/public/lm/lmromancaps10-regular.otf'

RNG = np.random.default_rng(1729)
GW, GH = W.GRID_W, W.GRID_H

KINGDOM_COL = {   # lowland, upland (RGB)
    'Elowen': ((104, 142, 78), (132, 150, 92)),
    'Isenmar': ((232, 238, 242), (204, 214, 226)),
    'Zenith': ((186, 170, 128), (204, 186, 142)),
    'Nadir': ((112, 116, 84), (128, 122, 96)),
    'Ossaria': ((222, 190, 128), (196, 140, 92)),
    'Ashkaar': ((112, 90, 78), (92, 76, 70)),
    'Crownhaven': ((228, 214, 168), (210, 196, 160)),
    'Antumbra': ((92, 78, 122), (70, 60, 100)),
}
BANNER = {'Elowen': (46, 110, 52), 'Isenmar': (64, 112, 156), 'Zenith': (196, 150, 40), 'Nadir': (92, 70, 110),
          'Ossaria': (190, 120, 50), 'Ashkaar': (170, 42, 30), 'Crownhaven': (230, 200, 90), 'Antumbra': (120, 90, 170)}
INK = (58, 42, 28)
PARCH = (233, 218, 178)


# ----------------------------------------------------------------------------- helpers
def fnoise(w, h, cells, seed, octaves=4, persist=0.5):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        cw = max(2, int(cells * (2 ** o)))
        ch = max(2, int(cw * h / w) + 1)
        g = rng.random((ch, cw)).astype(np.float32)
        im = Image.fromarray(g, 'F').resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(im)
        tot += amp
        amp *= persist
    out /= tot
    out -= out.min()
    out /= max(1e-6, out.max())
    return out


def poly_mask(polys, w, h, scale, ox=0.0, oy=0.0):
    im = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(im)
    for p in polys:
        d.polygon([((x - ox) * scale, (y - oy) * scale) for x, y in p], fill=255)
    return np.asarray(im) > 127


def warp_sample(mask, dx, dy):
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    sx = np.clip((xx + dx).round().astype(int), 0, w - 1)
    sy = np.clip((yy + dy).round().astype(int), 0, h - 1)
    return mask[sy, sx]


def seg_dist(px, py, pts):
    d = np.full(px.shape, 1e9, np.float32)
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        vx, vy = x2 - x1, y2 - y1
        L2 = vx * vx + vy * vy + 1e-9
        t = np.clip(((px - x1) * vx + (py - y1) * vy) / L2, 0, 1)
        dd = np.hypot(px - (x1 + t * vx), py - (y1 + t * vy))
        d = np.minimum(d, dd)
    return d


def catmull(pts, n=12):
    if len(pts) < 3:
        out = []
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            for i in range(n):
                t = i / n
                out.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
        out.append(pts[-1])
        return out
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 +
                                    (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def kingdoms_of(label):
    return label.split('/') if '/' in label else [label]


def cell_center(c):
    return (c[0] + 0.5, c[1] + 0.5)


def stop_points(stop):
    """centre points (grid units) of one stop in a ROAD_PATHS segment"""
    legs = W.leg_by_id()
    if isinstance(stop, int):
        if stop in W.SETTLEMENTS:
            n, x, y, r, k = W.SETTLEMENTS[stop]
            return [(x + 0.5, y + 0.5)]
        if stop in legs:
            return [cell_center(c) for c in legs[stop][1]['cells']]
    if isinstance(stop, str):
        if stop.startswith('sq:'):
            x, y = (int(v) for v in stop[3:].split(','))
            return [(x + 0.5, y + 0.5)]
        if stop.startswith('rev:'):
            return [cell_center(c) for c in reversed(legs[int(stop[4:])][1]['cells'])]
        if stop.startswith('P:'):
            return [cell_center(W.OWN_SQUARE[int(stop[2:])])]
        if stop.startswith('pts:'):
            return list(getattr(G, stop[4:]))
        if stop.startswith('G:'):
            return None
    raise KeyError(stop)


def ring_points(pts, n=96):
    """the Crown Road: a smooth closed ring through its squares (centred on the Crownwall)"""
    cx, cy = G.CROWNWALL['c']
    ang = [math.atan2(y - cy, x - cx) for x, y in pts[:-1]]
    rad = [math.hypot(x - cx, y - cy) for x, y in pts[:-1]]
    order = sorted(range(len(ang)), key=lambda i: ang[i])
    a_s = [ang[i] for i in order] + [ang[order[0]] + 2 * math.pi]
    r_s = [rad[i] for i in order] + [rad[order[0]]]
    out = []
    for k in range(n + 1):
        a = a_s[0] + (a_s[-1] - a_s[0]) * k / n
        j = max(i for i in range(len(a_s) - 1) if a_s[i] <= a + 1e-9) if a < a_s[-1] else len(a_s) - 2
        t = (a - a_s[j]) / (a_s[j + 1] - a_s[j])
        t = t * t * (3 - 2 * t)
        r = r_s[j] + (r_s[j + 1] - r_s[j]) * t
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def road_polylines():
    """yields (road n, style, [points]) with gates resolved per side (inset or real map)"""
    for n, segs in W.ROAD_PATHS.items():
        for style, stops in segs:
            pts = []
            for st in stops:
                if isinstance(st, str) and st.startswith('G:'):
                    real, inset, nm = W.GATES[st[2:]]
                    pts.append(cell_center(inset if style == 'inset' else real))
                else:
                    pts += stop_points(st)
            yield n, style, pts
    if getattr(W, 'CROWN_ROAD', None):
        pts = []
        for st in W.CROWN_ROAD:
            pts += stop_points(st)
        yield 0, 'ring', pts


def surface_kingdom(k):
    """Nadir lies beneath Zenith (Geography v2: the same footprint), so it has no surface zone of its own"""
    ks = ['Zenith' if x == 'Nadir' else x for x in k.split('/')]
    ks = list(dict.fromkeys(ks))
    return '/'.join(ks)


def zone_seeds():
    import json
    maps = {m['id']: m for m in json.load(open(os.path.join(ROOT, 'design', 'maps.json')))['maps']}
    seeds = []
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        if k != 'Antumbra':
            cx, cy = G.CROWNWALL['c']
            if 'Crownhaven' in k and k != 'Crownhaven' and math.hypot(x + 0.5 - cx, y + 0.5 - cy) > G.CROWNWALL['r'] + 1.2:
                k = 'Elowen'
            seeds.append((x + 0.5, y + 0.5, surface_kingdom(k)))
    for r, l in W.all_legs():
        if l['kingdom'] == 'Antumbra':
            continue
        for c in l['cells']:
            if c[0] >= 25 and c[1] >= 15:
                continue
            k = surface_kingdom(l['kingdom'])
            if 'Antumbra' in k:                  # gate borderlands take the colour of their real kingdom
                k = k.replace('Antumbra', '').strip('/')
            cx, cy = G.CROWNWALL['c']
            if 'Crownhaven' in k and math.hypot(c[0] + 0.5 - cx, c[1] + 0.5 - cy) > G.CROWNWALL['r'] + 1.2:
                k = 'Elowen'                     # the Pilgrim Pass is Accord ground on Elowen land
            seeds.append((c[0] + 0.5, c[1] + 0.5, k))
    for k, x, y in G.ANCHORS:
        seeds.append((x, y, k))
    return seeds


# ----------------------------------------------------------------------------- fields (shared by both renders)
class Fields:
    def __init__(self, scale):
        self.s = scale
        self.w, self.h = GW * scale, GH * scale
        w, h, s = self.w, self.h, scale
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        self.gx = (xx + 0.5) / s
        self.gy = (yy + 0.5) / s
        amp = 0.16 * s
        n1 = fnoise(w, h, 7, 11, 5) - 0.5
        n2 = fnoise(w, h, 7, 12, 5) - 0.5
        n3 = fnoise(w, h, 40, 13, 3) - 0.5
        n4 = fnoise(w, h, 40, 14, 3) - 0.5
        self.dx = n1 * 2 * amp + n3 * 0.09 * s
        self.dy = n2 * 2 * amp + n4 * 0.09 * s
        land = poly_mask([G.MAINLAND] + G.ISLANDS, w, h, s)
        self.land = warp_sample(land, self.dx, self.dy)
        lakes = {}
        for nm, L in G.LAKES.items():
            lakes[nm] = warp_sample(poly_mask([L['poly']], w, h, s), self.dx * 0.4, self.dy * 0.4) & self.land
        self.lakes = lakes
        self.water_in = np.zeros_like(self.land)
        for m in lakes.values():
            self.water_in |= m
        self.sea = ~self.land
        self.dist_sea = ndimage.distance_transform_edt(self.land) / s    # land: distance to sea (grid units)
        self.dist_land = ndimage.distance_transform_edt(self.sea) / s    # sea: distance to land
        # elevation
        gx, gy = self.gx, self.gy
        base = fnoise(w, h, 5, 21, 5)
        elev = base * 0.22
        plat = poly_mask([G.PLATEAU], w, h, s)
        plat = warp_sample(plat, self.dx * 0.7, self.dy * 0.7)
        self.plateau = plat & self.land
        pb = ndimage.gaussian_filter(plat.astype(np.float32), 0.05 * s)
        elev += pb * 0.6
        rnoise = fnoise(w, h, 9, 22, 4)
        self.ridge = np.zeros((h, w), np.float32)
        for pts, hgt, wid in G.RIDGES:
            d = seg_dist(gx, gy, pts)
            r = hgt * np.exp(-(d / wid) ** 2) * (0.55 + 0.9 * rnoise)
            self.ridge = np.maximum(self.ridge, r)
        vx, vy = G.VOLCANO
        dv = np.hypot(gx - vx, gy - vy)
        self.volc = 1.25 * np.exp(-(dv / 0.75) ** 2)
        cx, cy = G.CROWNWALL['c']
        dr = np.hypot(gx - cx, gy - cy)
        ang = np.degrees(np.arctan2(gy - cy, gx - cx))
        gd_ = np.abs(((ang - G.CROWNWALL['gap_angle']) + 180) % 360 - 180)
        gapf = 0.25 + 0.75 * np.clip((gd_ - 8) / 22.0, 0, 1)        # soft-edged pass through the ring
        ring = 1.0 * np.exp(-((dr - G.CROWNWALL['r']) / G.CROWNWALL['w']) ** 2) * (0.7 + 0.5 * rnoise) * gapf
        self.ring = ring
        elev = elev + self.ridge + self.volc + ring
        elev *= np.clip(self.dist_sea / 0.6, 0.25, 1.0)
        self.elev = np.where(self.land, elev, 0).astype(np.float32)
        # zones
        seeds = zone_seeds()
        tree = cKDTree([(x, y) for x, y, k in seeds])
        zn1 = (fnoise(w, h, 6, 31, 4) - 0.5) * 1.1
        zn2 = (fnoise(w, h, 6, 32, 4) - 0.5) * 1.1
        q = np.stack([(gx + zn1).ravel(), (gy + zn2).ravel()], 1)
        _, idx = tree.query(q)
        labels = sorted({k for _, _, k in seeds})
        self.labels = labels
        lab_of_seed = np.array([labels.index(k) for _, _, k in seeds])
        self.zone = lab_of_seed[idx].reshape(h, w)
        self.mixn = fnoise(w, h, 14, 41, 4)
        self.grain = fnoise(w, h, 60, 42, 3)
        self.forest = self._density(G.FORESTS, 43)
        self.marsh = self._density([(x, y, r, 'm') for x, y, r in G.MARSHES], 44)
        self.dunes = self._density([(x, y, r, 'd') for x, y, r in G.DESERT_DUNES], 45)
        self.obsid = self._density([(x, y, r, 'o') for x, y, r in G.OBSIDIAN], 46)
        self.sulfur = self._density([(x, y, r, 's') for x, y, r in G.SULFUR], 47)
        xmax = getattr(G, 'FROZEN_SEA_X_MAX', 26.6)
        edge = fnoise(w, h, 9, 48, 4) - 0.5
        self.frozen = self.sea & (gy + edge * 0.8 < G.FROZEN_SEA_EDGE_Y) & (gx + edge * 1.2 < xmax)
        if G.SHATTERED_ICE:
            x0, y0, x1, y1 = G.SHATTERED_ICE
            self.shattered = self.sea & (gx > x0) & (gx < x1) & (gy > y0 - 1.5) & (gy < y1)
        else:
            self.shattered = np.zeros_like(self.sea)
        self.forest_kind = self._kind_map()

    def _density(self, items, seed):
        n = fnoise(self.w, self.h, 10, seed, 4)
        d = np.zeros((self.h, self.w), np.float32)
        for it in items:
            x, y, r = it[0], it[1], it[2]
            dd = np.hypot(self.gx - x, self.gy - y) / r
            d = np.maximum(d, np.clip(1.25 - dd, 0, 1))
        return d * (0.55 + 0.7 * n)

    def _kind_map(self):
        best = np.full((self.h, self.w), -1, np.int16)
        bestv = np.zeros((self.h, self.w), np.float32)
        kinds = sorted({f[3] for f in G.FORESTS})
        self.fkinds = kinds
        for x, y, r, k in G.FORESTS:
            v = np.clip(1.3 - np.hypot(self.gx - x, self.gy - y) / r, 0, None)
            m = v > bestv
            best[m] = kinds.index(k)
            bestv[m] = v[m]
        return best

    def zone_name(self, iy, ix):
        return self.labels[self.zone[iy, ix]]


# ----------------------------------------------------------------------------- painted world map
def font(path, size):
    return ImageFont.truetype(path, int(size))


def text_halo(d, xy, txt, f, fill, halo=(240, 228, 196), hw=3, anchor='mm', spacing=0):
    if spacing:
        txt = (' ' * 0).join(txt)
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=hw, stroke_fill=halo)


def spaced(txt, n=1):
    return (' ' * n).join(txt)


class Labels:
    def __init__(self, w, h):
        self.boxes = []
        self.w, self.h = w, h

    def free(self, box, pad=2):
        x0, y0, x1, y1 = box
        if x0 < 4 or y0 < 4 or x1 > self.w - 4 or y1 > self.h - 4:
            return False
        for b in self.boxes:
            if not (x1 + pad < b[0] or x0 - pad > b[2] or y1 + pad < b[1] or y0 - pad > b[3]):
                return False
        return True

    def add(self, box):
        self.boxes.append(box)


def paint_big(out_path):
    S = 80
    F = Fields(S)
    w, h = F.w, F.h
    gx, gy = F.gx, F.gy
    print('fields ready', w, h)
    col = np.zeros((h, w, 3), np.float32)
    # --- land colours by zone (borderlands mottle both kingdoms)
    lab_cols = []
    for lab in F.labels:
        ks = kingdoms_of(lab)
        lab_cols.append([np.array(KINGDOM_COL[k][0], np.float32) for k in ks])
    up = np.clip(F.elev / 0.9, 0, 1)[..., None]
    for li, lab in enumerate(F.labels):
        m = F.zone == li
        if not m.any():
            continue
        ks = kingdoms_of(lab)
        lo = np.array(KINGDOM_COL[ks[0]][0], np.float32)
        hi = np.array(KINGDOM_COL[ks[0]][1], np.float32)
        c = lo * (1 - up) + hi * up
        if len(ks) == 2:
            lo2 = np.array(KINGDOM_COL[ks[1]][0], np.float32)
            hi2 = np.array(KINGDOM_COL[ks[1]][1], np.float32)
            c2 = lo2 * (1 - up) + hi2 * up
            t = np.clip((F.mixn - 0.5) * 9.0 + 0.5, 0.0, 1.0)[..., None]
            c = c * (1 - t) + c2 * t
        col[m] = c[m]
    # biome overlays
    def over(mask_f, rgb, a=1.0):
        t = np.clip(mask_f, 0, 1)[..., None] * a
        col[:] = col * (1 - t) + np.array(rgb, np.float32) * t
    over((F.forest - 0.35) * 1.6 * F.land, (70, 104, 60), 0.55)
    over((F.dunes - 0.3) * 1.5 * F.land, (230, 198, 132), 0.5)
    over((F.marsh - 0.3) * 1.6 * F.land, (96, 108, 70), 0.6)
    over((F.obsid - 0.3) * 1.6 * F.land, (46, 40, 48), 0.75)
    over((F.sulfur - 0.35) * 1.6 * F.land, (206, 188, 84), 0.45)
    over(np.clip((F.elev - 0.75) * 2.0, 0, 1) * F.land, (238, 238, 236), 0.75)    # snowy peaks
    over(np.clip(F.plateau * 1.0, 0, 1) * 0.0, (0, 0, 0), 0)
    # Isenmar and the Rimewood are white: keep them crisp
    # glacier
    glac = warp_sample(poly_mask([G.GLACIER], w, h, S), F.dx * 0.5, F.dy * 0.5)
    over(glac.astype(np.float32), (226, 238, 244), 0.85)
    # lava veins near the Cinderhorn
    lav = fnoise(w, h, 22, 51, 3)
    vein = (np.abs(lav - 0.5) < 0.018) & (np.hypot(gx - G.VOLCANO[0], gy - G.VOLCANO[1]) < 2.2) & F.land
    col[vein] = col[vein] * 0.3 + np.array((222, 84, 32), np.float32) * 0.7
    # hillshade
    e = ndimage.gaussian_filter(F.elev, 1.2)
    gyv, gxv = np.gradient(e)
    shade = np.clip(0.5 + (-gxv - gyv) * 45.0, 0, 1)
    col *= (0.72 + 0.56 * shade)[..., None]
    # escarpment: darker rim around the plateau
    pe = F.plateau.astype(np.float32)
    col *= (1 + 0.07 * ndimage.gaussian_filter(pe, 2))[..., None]
    # the Escarpment: a rock band round the plateau, lit from the north-west, with an ink lip and foot
    din = ndimage.distance_transform_edt(F.plateau) / S
    bw = 0.08 + 0.09 * fnoise(w, h, 20, 82, 2)
    band = F.plateau & (din < bw)
    gyp, gxp = np.gradient(ndimage.gaussian_filter(pe, 0.12 * S))
    nrm = np.hypot(gxp, gyp) + 1e-6
    light = np.clip(0.5 + ((-gxp) * -0.7 + (-gyp) * -0.7) / nrm * 0.6, 0, 1)
    stri = fnoise(w, h, 140, 81, 2)
    rock = np.array((200, 180, 144), np.float32)[None, None, :] * \
        ((0.62 + 0.5 * light) * (0.8 + 0.3 * stri) * (0.8 + 0.25 * np.clip(din / 0.15, 0, 1)))[..., None]
    col[band] = rock[band]
    lip = F.plateau & (din >= bw) & (din < bw + 2.0 / S)
    col[lip] *= 0.62
    foot = F.plateau & (din < 1.5 / S)
    col[foot] *= 0.6
    # --- water
    dl = F.dist_land
    deep = np.array((54, 92, 112), np.float32)
    shallow = np.array((118, 166, 172), np.float32)
    t = np.clip(dl / 2.2, 0, 1)[..., None]
    seacol = shallow * (1 - t) + deep * t
    ripple = (np.abs(((dl * 6.0 + F.grain * 0.4) % 1.0) - 0.5) < 0.05) & (dl < 1.4)
    seacol[ripple] = seacol[ripple] * 0.86 + 255 * 0.14
    ice = np.array((228, 238, 242), np.float32)
    seacol[F.frozen] = ice * (0.92 + 0.08 * F.grain[F.frozen][..., None])
    fy, fx = np.nonzero(F.frozen)
    fpts = RNG.random((900, 2)) * np.array([GW, 3.6])
    ftree = cKDTree(fpts)
    dd, ii = ftree.query(np.stack([F.gx[fy, fx] + F.dx[fy, fx] / S * 0.3, F.gy[fy, fx]], 1), k=2)
    tone = RNG.random(len(fpts))[ii[:, 0]]
    seacol[fy, fx] = np.array((222, 236, 244), np.float32) * (0.95 + 0.06 * tone)[:, None]
    ck = (dd[:, 1] - dd[:, 0]) < 0.022
    seacol[fy[ck], fx[ck]] = (150, 182, 206)
    crack = np.zeros_like(F.frozen)
    iedge = F.frozen & ~ndimage.binary_erosion(F.frozen, iterations=3) & (F.dist_land > 0.1)
    seacol[iedge] = (250, 252, 252)
    floes = F.shattered & (fnoise(w, h, 30, 53, 2) > 0.56)
    seacol[floes] = (224, 236, 240)
    col[F.sea] = seacol[F.sea]
    for nm, m in F.lakes.items():
        kind = G.LAKES[nm]['kind']
        c = {'sulfur': (196, 182, 90), 'mirror': (196, 204, 214), 'salt': (170, 204, 210), 'frozen': (220, 232, 238)}[kind]
        col[m] = np.array(c, np.float32) * (0.9 + 0.1 * F.grain[m][..., None])
    # --- parchment blend and grain
    parch = np.array(PARCH, np.float32)
    paper = fnoise(w, h, 3, 61, 6)
    col = col * 0.86 + parch * 0.14
    col *= (0.93 + 0.1 * paper)[..., None]
    col *= (0.96 + 0.06 * F.grain)[..., None]
    # vignette
    vx = (gx / GW - 0.5) * 2
    vy = (gy / GH - 0.5) * 2
    vig = np.clip(1 - 0.18 * (vx ** 2 + vy ** 2) ** 1.4, 0.75, 1)
    col *= vig[..., None]
    img = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), 'RGB')
    # --- coastline ink
    edge = F.land ^ ndimage.binary_erosion(F.land, iterations=2)
    edge2 = F.sea & ndimage.binary_dilation(F.land, iterations=4) & ~ndimage.binary_dilation(F.land, iterations=2)
    arr = np.asarray(img).copy()
    arr[edge2] = (arr[edge2] * 0.75 + np.array((235, 238, 226)) * 0.25).astype(np.uint8)
    arr[edge] = (arr[edge] * 0.25 + np.array(INK) * 0.75).astype(np.uint8)
    for m in F.lakes.values():
        le = m ^ ndimage.binary_erosion(m, iterations=1)
        arr[le] = (arr[le] * 0.35 + np.array(INK) * 0.65).astype(np.uint8)
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img, 'RGBA')
    P = lambda x, y: (x * S, y * S)

    # --- kingdom borders (zone label changes between two different pure kingdoms or into a borderland)
    z = F.zone
    bd = np.zeros_like(F.land)
    bd[:, 1:] |= z[:, 1:] != z[:, :-1]
    bd[1:, :] |= z[1:, :] != z[:-1, :]
    bd &= F.land & (F.dist_sea > 0.08)
    bd = ndimage.binary_dilation(bd, iterations=1)
    dash = ((gx * 3.2 + gy * 3.2) % 1.0) < 0.6
    arr = np.asarray(img).copy()
    m = bd & dash
    arr[m] = (arr[m] * 0.45 + np.array((120, 40, 40)) * 0.55).astype(np.uint8)
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img, 'RGBA')

    keep = np.zeros((h, w), bool)   # keep-out mask for glyphs (roads, towns, rivers)
    road_lines = []
    for n, style, pts in road_polylines():
        if style == 'inset':
            continue
        if style == 'ring':
            pts = ring_points(pts)
        road_lines.append((n, style, catmull(pts, 14) if style not in ('ring',) else pts))
    kd = Image.new('L', (w, h), 0)
    kdd = ImageDraw.Draw(kd)
    for n, style, line in road_lines:
        kdd.line([P(*p) for p in line], fill=255, width=26)
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        if k == 'Antumbra':
            continue
        kdd.ellipse([P(x + 0.5 - 0.42, y + 0.5 - 0.42), P(x + 0.5 + 0.42, y + 0.5 + 0.42)], fill=255)
    for nm, rv in G.RIVERS.items():
        kdd.line([P(*p) for p in catmull(rv['pts'], 10)], fill=255, width=12)
    keep = np.asarray(kd) > 0
    keep |= F.water_in

    # --- rivers
    for nm, rv in G.RIVERS.items():
        line = catmull(rv['pts'], 16)
        n = len(line)
        c = (70, 120, 150) if rv['kind'] == 'water' else (60, 200, 210)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            wd = (rv['w'][0] + (rv['w'][1] - rv['w'][0]) * t) * S
            d.line([P(*line[i]), P(*line[i + 1])], fill=c + (255,), width=max(2, int(wd)))
        if rv['kind'] == 'toxic':
            for i in range(0, n - 1, 2):
                d.line([P(*line[i]), P(*line[i + 1])], fill=(140, 255, 240, 140), width=2)
    bl = catmull(G.BLINDWATER, 18)
    for i in range(0, len(bl) - 1, 3):
        pass

    # --- glyphs
    glyph = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glyph)
    items = []
    sp = 15
    for y0 in range(0, h, sp):
        for x0 in range(0, w, sp):
            x = x0 + RNG.integers(-5, 6)
            y = y0 + RNG.integers(-5, 6)
            if not (0 <= x < w and 0 <= y < h):
                continue
            if not F.land[y, x] or keep[y, x] or F.dist_sea[y, x] < 0.12:
                continue
            fv = F.forest[y, x]
            if fv > 0.42 and RNG.random() < min(1.0, (fv - 0.3) * 2.2):
                items.append((y, x, 'tree', F.fkinds[F.forest_kind[y, x]] if F.forest_kind[y, x] >= 0 else 'broad'))
    # mountains along ridges and the ring/volcano
    for pts, hgt, wid in G.RIDGES:
        line = catmull(pts, 30)
        acc = 0
        for i in range(len(line) - 1):
            acc += math.hypot(line[i + 1][0] - line[i][0], line[i + 1][1] - line[i][1])
            if acc > 0.26 / max(0.6, hgt):
                acc = 0
                for k in range(1 if hgt < 0.7 else 2):
                    ox = RNG.normal(0, wid * 0.35)
                    oy = RNG.normal(0, wid * 0.35)
                    x, y = int((line[i][0] + ox) * S), int((line[i][1] + oy) * S)
                    if 0 <= x < w and 0 <= y < h and F.land[y, x] and not keep[y, x]:
                        items.append((y, x, 'peak', hgt * (0.7 + 0.5 * RNG.random())))
    cx, cy = G.CROWNWALL['c']
    for a in range(0, 360, 14):
        if abs(((a - G.CROWNWALL['gap_angle']) + 180) % 360 - 180) < 18:
            continue
        r = G.CROWNWALL['r'] + RNG.normal(0, 0.08)
        x, y = int((cx + r * math.cos(math.radians(a))) * S), int((cy + r * math.sin(math.radians(a))) * S)
        if not keep[min(h - 1, y), min(w - 1, x)]:
            items.append((y, x, 'peak', 0.8))
    items.append((int(G.VOLCANO[1] * S), int(G.VOLCANO[0] * S), 'volcano', 1.0))
    # dunes, marsh tufts, snow sparkles, ice pines
    for y0 in range(0, h, 22):
        for x0 in range(0, w, 22):
            x = x0 + RNG.integers(-8, 9)
            y = y0 + RNG.integers(-8, 9)
            if not (0 <= x < w and 0 <= y < h) or not F.land[y, x] or keep[y, x]:
                continue
            ks = kingdoms_of(F.zone_name(y, x))
            k0 = ks[0] if len(ks) == 1 or F.mixn[y, x] < 0.5 else ks[1]
            free = F.forest[y, x] < 0.35 and F.ridge[y, x] < 0.3 and F.ring[y, x] < 0.25
            rr = RNG.random()
            if F.dunes[y, x] > 0.5 and rr < 0.6:
                items.append((y, x, 'dune', 0))
            elif F.marsh[y, x] > 0.45 and rr < 0.7:
                items.append((y, x, 'tuft' if rr < 0.5 else 'pool', 0))
            elif F.obsid[y, x] > 0.45 and rr < 0.5:
                items.append((y, x, 'shard', 0))
            elif free and F.elev[y, x] > 0.32 and not F.plateau[y, x] and rr < 0.16:
                items.append((y, x, 'hill', 0))
            elif not free:
                continue
            elif k0 == 'Elowen' and rr < 0.07:
                items.append((y, x, 'clump', 'broad'))
            elif k0 == 'Elowen' and rr < 0.11 and F.dist_sea[y, x] > 0.4:
                items.append((y, x, 'field', 0))
            elif k0 == 'Isenmar' and rr < 0.08:
                items.append((y, x, 'tree', 'pine'))
            elif k0 == 'Isenmar' and rr < 0.2:
                items.append((y, x, 'drift', 0))
            elif k0 == 'Ossaria' and rr < 0.3:
                items.append((y, x, 'dune', 0))
            elif k0 == 'Ossaria' and rr < 0.34:
                items.append((y, x, 'mesa', 0))
            elif k0 == 'Nadir' and rr < 0.12:
                items.append((y, x, 'tuft', 0))
            elif k0 == 'Nadir' and rr < 0.16:
                items.append((y, x, 'heap', 0))
            elif k0 == 'Ashkaar' and rr < 0.06:
                items.append((y, x, 'cone', 0))
            elif k0 == 'Ashkaar' and rr < 0.2:
                items.append((y, x, 'ash', 0))
            elif k0 == 'Zenith' and F.plateau[y, x] and rr < 0.05:
                items.append((y, x, 'pylon', 0))
            elif k0 == 'Zenith' and not F.plateau[y, x] and rr < 0.1:
                items.append((y, x, 'field', 0))
    # escarpment hachures around the plateau
    pe_edge = F.plateau ^ ndimage.binary_erosion(F.plateau, iterations=2)
    ys, xs = np.nonzero(pe_edge)
    sel = RNG.random(len(xs)) < 0.0
    ny, nx = np.gradient(ndimage.gaussian_filter(F.plateau.astype(np.float32), 4))
    for y, x in zip(ys[sel], xs[sel]):
        if keep[y, x]:
            continue
        vx_, vy_ = -nx[y, x], -ny[y, x]
        L = math.hypot(vx_, vy_) + 1e-6
        items.append((y, x, 'hach', (vx_ / L, vy_ / L)))
    items.sort(key=lambda it: it[0])
    for y, x, kind, arg in items:
        if kind == 'tree':
            draw_tree(gd, x, y, arg, F.zone_name(y, x))
        elif kind == 'peak':
            draw_peak(gd, x, y, arg, F.zone_name(y, x))
        elif kind == 'volcano':
            draw_volcano(gd, x, y)
        elif kind == 'dune':
            gd.arc([x - 9, y - 4, x + 9, y + 6], 200, 340, fill=(150, 104, 60, 200), width=2)
        elif kind == 'tuft':
            for k in (-4, 0, 4):
                gd.line([(x, y + 3), (x + k, y - 4)], fill=(52, 70, 40, 220), width=1)
            gd.line([(x - 6, y + 4), (x + 6, y + 4)], fill=(80, 120, 120, 160), width=1)
        elif kind == 'shard':
            gd.polygon([(x - 4, y + 4), (x, y - 7), (x + 3, y + 4)], fill=(30, 26, 36, 230), outline=(120, 110, 150, 255))
        elif kind == 'hill':
            gd.chord([x - 11, y - 6, x + 11, y + 10], 180, 360, fill=(0, 0, 0, 28))
            gd.arc([x - 11, y - 6, x + 11, y + 10], 190, 350, fill=INK + (150,), width=2)
        elif kind == 'clump':
            for ox, oy in ((-5, 1), (4, 2), (0, -3))[:RNG.integers(1, 4)]:
                draw_tree(gd, x + ox, y + oy, 'broad', '')
        elif kind == 'field':
            ang = RNG.random() * 0.8 - 0.4
            cw, ch = 16, 10
            c = [(60, 120, 50), (150, 150, 70), (180, 160, 90), (110, 140, 60)][RNG.integers(0, 4)]
            pts = [(x - cw / 2, y - ch / 2), (x + cw / 2, y - ch / 2 + ang * 8), (x + cw / 2, y + ch / 2 + ang * 8),
                   (x - cw / 2, y + ch / 2)]
            gd.polygon(pts, fill=c + (120,), outline=(90, 80, 50, 110))
            for k in range(-3, 4, 3):
                gd.line([(x - cw / 2 + 2, y + k), (x + cw / 2 - 2, y + k + ang * 8)], fill=(80, 70, 40, 70), width=1)
        elif kind == 'drift':
            gd.arc([x - 9, y - 3, x + 9, y + 7], 200, 330, fill=(150, 170, 190, 170), width=2)
            gd.arc([x - 9, y - 1, x + 9, y + 9], 200, 330, fill=(255, 255, 255, 200), width=1)
        elif kind == 'mesa':
            gd.polygon([(x - 10, y + 5), (x - 6, y - 4), (x + 6, y - 4), (x + 10, y + 5)], fill=(190, 124, 80, 230),
                       outline=INK + (200,))
            gd.line([(x - 6, y - 4), (x + 6, y - 4)], fill=(236, 190, 130, 255), width=2)
        elif kind == 'heap':
            gd.pieslice([x - 8, y - 6, x + 8, y + 8], 180, 360, fill=(110, 104, 96, 230), outline=INK + (180,))
        elif kind == 'pool':
            gd.ellipse([x - 6, y - 3, x + 6, y + 3], fill=(120, 190, 120, 200), outline=(50, 70, 40, 200))
        elif kind == 'cone':
            gd.polygon([(x - 9, y + 5), (x - 3, y - 6), (x + 3, y - 6), (x + 9, y + 5)], fill=(76, 62, 58, 240),
                       outline=INK + (220,))
            gd.line([(x - 3, y - 6), (x + 3, y - 6)], fill=(230, 100, 40, 255), width=2)
        elif kind == 'ash':
            gd.line([(x - 7, y), (x + 7, y - 2)], fill=(70, 60, 56, 120), width=2)
        elif kind == 'pylon':
            gd.line([(x, y + 6), (x, y - 10)], fill=(90, 74, 50, 220), width=2)
            gd.line([(x - 5, y - 7), (x + 5, y - 7)], fill=(90, 74, 50, 220), width=2)
            gd.line([(x - 4, y + 6), (x, y - 4), (x + 4, y + 6)], fill=(90, 74, 50, 200), width=1)
        elif kind == 'plot':
            gd.rectangle([x - 7, y - 5, x + 7, y + 5], outline=(130, 110, 70, 90), width=1)
            gd.line([(x, y - 5), (x, y + 5)], fill=(130, 110, 70, 70), width=1)
        elif kind == 'hach':
            vx_, vy_ = arg
            lit = (vx_ * -0.7 + vy_ * -0.7) > 0
            gd.line([(x, y), (x + vx_ * 15, y + vy_ * 15)], fill=(120, 96, 64, 150) if lit else (66, 48, 34, 210),
                    width=2 if lit else 3)
    img = Image.alpha_composite(img.convert('RGBA'), glyph)
    d = ImageDraw.Draw(img, 'RGBA')

    # --- sea lanes and air lanes
    for pts, kind, lab in G.SEA_LANES:
        line = catmull(pts, 20)
        c = {'ferry': (40, 60, 90, 200), 'sled': (90, 110, 130, 200), 'war': (170, 40, 30, 230)}[kind]
        for i in range(0, len(line) - 1, 2):
            d.line([P(*line[i]), P(*line[i + 1])], fill=c, width=3 if kind != 'war' else 4)
    for pts in G.AIR_LANES:
        line = catmull(pts, 30)
        for i in range(0, len(line) - 1, 3):
            d.line([P(*line[i]), P(*line[i + 1])], fill=(250, 250, 255, 170), width=2)

    # --- roads
    for n, style, line in road_lines:
        pl = [P(*p) for p in line]
        if style == 'air':
            for i in range(0, len(pl) - 1, 3):
                d.line([pl[i], pl[i + 1]], fill=(40, 60, 96, 200), width=6)
                d.line([pl[i], pl[i + 1]], fill=(250, 250, 255, 235), width=3)
            continue
        if style == 'under':
            for i in range(0, len(pl) - 1, 3):
                d.line([pl[i], pl[i + 1]], fill=(50, 40, 60, 70), width=3)
            continue
        if style == 'sea':
            for i in range(0, len(pl) - 1, 2):
                d.line([pl[i], pl[i + 1]], fill=(40, 60, 90, 220), width=4)
            continue
        wdt = 7 if style in ('road', 'ring') else 5
        d.line(pl, fill=(60, 40, 22, 235), width=wdt + 4, joint='curve')
        d.line(pl, fill=(236, 214, 160, 255) if style in ('road', 'ring') else (214, 196, 150, 255), width=wdt,
               joint='curve')

    # --- the war in the sands (Revision 18): marches, the front (the Steamline) and the battlefield
    if getattr(G, 'WAR', None):
        draw_war_big(d, P, S)
    # --- Antumbra gates on the real map
    for g, (real, inset, nm) in W.GATES.items():
        x, y = P(*cell_center(real))
        draw_gate(d, x, y, g)

    # --- towns, gym badges and road shields (placed first: they never move)
    LB = Labels(w, h)
    ix0, iy0, ix1, iy1 = W.ANTUMBRA_INSET
    LB.add((ix0 * S - 10, iy0 * S - 10, w, h))          # the Antumbra inset covers this corner
    fT = font(F_SERIF_B, 25)
    fTs = font(F_SERIF_B, 21)
    fV = font(F_SERIF, 19)
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        if k == 'Antumbra':
            continue
        cxp, cyp = P(x + 0.5, y + 0.5)
        LB.add(draw_town(d, cxp, cyp, r, k))
    fG = font(F_SERIF_B, 17)
    for gi, tid in enumerate(W.GYMS, 1):
        n, x, y, r, k = W.SETTLEMENTS[tid]
        if k == 'Antumbra':
            continue
        cxp, cyp = P(x + 0.5, y + 0.5)
        draw_gym_badge(d, cxp + 22, cyp - 22, gi, fG)
        LB.add((cxp + 9, cyp - 35, cxp + 35, cyp - 9))
    fRn = font(F_SERIF_BI, 19)
    for rd in W.ROADS:
        main = [l for l in rd['legs'] if l['role'] == 'main' and not (l['cells'][0][0] >= 25 and l['cells'][0][1] >= 15)]
        if not main:
            continue
        c = main[len(main) // 2]['cells'][0]
        x, y = P(*cell_center(c))
        draw_road_shield(d, x, y, rd['n'], fRn)
        LB.add((x - 14, y - 14, x + 14, y + 16))
    for g, (real, inset, nm) in W.GATES.items():
        x, y = P(*cell_center(real))
        LB.add((x - 14, y - 18, x + 14, y + 18))
    # --- town names
    order = sorted(W.SETTLEMENTS.items(), key=lambda kv: {'seat': 0, 'city': 1, 'fort': 2, 'town': 3, 'village': 4}[kv[1][3]])
    for i, (n, x, y, r, k) in order:
        if k == 'Antumbra':
            continue
        cxp, cyp = P(x + 0.5, y + 0.5)
        f = fT if r == 'seat' else (fTs if r in ('city', 'fort') else fV)
        txt = n.upper() if r == 'seat' else n
        if i == 480:
            d.text((cxp, cyp + 34), 'CROWNHAVEN', font=font(F_CAPS, 30), fill=(70, 34, 22), anchor='mm', stroke_width=3,
                   stroke_fill=(244, 236, 210))
            d.text((cxp, cyp + 60), "the Accord's seat and the Festival", font=font(F_SERIF_I, 18), fill=INK, anchor='mm',
                   stroke_width=3, stroke_fill=(244, 236, 210))
            LB.add((cxp - 110, cyp + 18, cxp + 110, cyp + 72))
            continue
        place_label(d, LB, txt, f, cxp, cyp, 26, (34, 22, 14),
                    [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (-1, -1), (1, 1), (-1, 1)])
    # --- kingdom names: big, translucent, auto-placed where the kingdom has the most empty land
    kl = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    kd2 = ImageDraw.Draw(kl)
    KSIZE = {'ISENMAR': 44, 'NADIR': 38, 'ZENITH': 46}
    fKs = font(F_SERIF_I, 26)
    busy = keep.astype(np.float32)
    for b in LB.boxes:
        busy[int(max(0, b[1])):int(max(0, b[3])), int(max(0, b[0])):int(max(0, b[2]))] = 1.0
    ib_ = [busy.cumsum(0).cumsum(1)]

    def busy_sum(x0, y0, x1, y1):
        ib = ib_[0]
        if x0 < 8 or y0 < 8 or x1 > w - 8 or y1 > h - 8:
            return 1e9
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        return ib[y1, x1] - ib[y0, x1] - ib[y1, x0] + ib[y0, x0]
    for nm, sub, x, y in G.KINGDOM_LABELS:
        if nm == 'CROWNHAVEN':
            continue
        if nm == 'ISENMAR':         # the kingdom IS the frozen sea: its name sits on the ice
            fK = font(F_CAPS, 50)
            kd2.text(P(x, y), spaced(nm, 1), font=fK, fill=(40, 60, 84, 190), anchor='mm', stroke_width=2,
                     stroke_fill=(236, 244, 248, 160))
            kd2.text((P(x, y)[0], P(x, y)[1] + 34), sub, font=fKs, fill=(40, 60, 84, 210), anchor='mm', stroke_width=2,
                     stroke_fill=(236, 244, 248, 170))
            tb = kd2.textbbox(P(x, y), spaced(nm, 1), font=fK, anchor='mm')
            LB.add((tb[0], tb[1], tb[2], tb[3] + 46))
            continue
        fK = font(F_CAPS, KSIZE.get(nm, 58))
        tb = kd2.textbbox((0, 0), spaced(nm, 1), font=fK, anchor='mm')
        tw, th = tb[2] - tb[0], tb[3] - tb[1] + 54
        best = None
        if nm in getattr(G, 'KINGDOM_LABELS_FIXED', ()):     # hand-placed (crowded kingdoms)
            best = (0, x * S, y * S)
        ki = [i for i, lab in enumerate(F.labels) if lab == nm.title()]
        for oy in (np.arange(-1.6, 1.61, 0.2) if best is None else []):
            for ox in np.arange(-2.4, 2.41, 0.2):
                cx_, cy_ = (x + ox) * S, (y + oy) * S
                if not (0 <= int(cx_) < w and 0 <= int(cy_) < h) or not F.land[int(cy_), int(cx_)]:
                    continue
                if ki and F.zone[int(cy_), int(cx_)] != ki[0]:
                    continue
                sc = busy_sum(cx_ - tw / 2, cy_ - th / 2 + 10, cx_ + tw / 2, cy_ + th / 2) + (ox * ox + oy * oy) * 900
                if best is None or sc < best[0]:
                    best = (sc, cx_, cy_)
        if best is None:
            continue
        cx_, cy_ = best[1], best[2]
        kd2.text((cx_, cy_), spaced(nm, 1), font=fK, fill=(60, 36, 24, 165), anchor='mm', stroke_width=2,
                 stroke_fill=(240, 228, 196, 120))
        kd2.text((cx_, cy_ + 40), sub, font=fKs, fill=(60, 36, 24, 200), anchor='mm', stroke_width=2,
                 stroke_fill=(240, 228, 196, 150))
        box = (cx_ - tw / 2, cy_ - th / 2 + 10, cx_ + tw / 2, cy_ + th / 2 + 6)
        LB.add(box)
        busy[int(max(0, box[1])):int(max(0, box[3])), int(max(0, box[0])):int(max(0, box[2]))] = 1.0   # later labels avoid it
        ib_[0] = busy.cumsum(0).cumsum(1)
    img = Image.alpha_composite(img, kl)
    d = ImageDraw.Draw(img, 'RGBA')
    # --- landmarks (nudged off anything already placed) and seas
    for nm, x, y, sz, a in G.LANDMARKS:
        f = font(F_SERIF_I, 44 * sz)
        for ox, oy in ((0, 0), (0, 0.3), (0, -0.3), (0.4, 0), (-0.4, 0), (0.4, 0.4), (-0.4, -0.4), (0, 0.6), (0, -0.6)):
            box = rot_box(P(x + ox, y + oy), nm, f, a)
            if LB.free(box, pad=0):
                draw_rot_text(img, P(x + ox, y + oy), nm, f, (70, 46, 30, 235), a, halo=(240, 230, 200, 170))
                LB.add(box)
                break
        else:
            print('  landmark dropped:', nm)
    for nm, x, y, sz in (G.WAR['labels'] if getattr(G, 'WAR', None) else []):
        f = font(F_SERIF_BI, 44 * sz)
        for ox, oy in ((0, 0), (0, 0.25), (0, -0.25), (0.35, 0), (-0.35, 0)):
            box = rot_box(P(x + ox, y + oy), nm, f, 0)
            if LB.free(box, pad=0):
                draw_rot_text(img, P(x + ox, y + oy), nm, f, (130, 22, 16, 245), 0, halo=(244, 234, 206, 200))
                LB.add(box)
                break
        else:
            print('  war label dropped:', nm)
    d = ImageDraw.Draw(img, 'RGBA')
    for nm, x, y, a, sz in G.SEAS:
        f = font(F_SERIF_I, 34 * sz + 6)
        draw_rot_text(img, P(x, y), spaced(nm, 1) if nm.isupper() else nm, f, (30, 56, 80, 230), a,
                      halo=(214, 228, 232, 150))
    d = ImageDraw.Draw(img, 'RGBA')
    # --- road names (one per leg)
    fR = font(F_SERIF_I, 17)
    lm_names = {nm.lower().replace('the ', '') for nm, *_ in G.LANDMARKS}
    for r, l in W.all_legs():
        cells = [c for c in l['cells'] if not (c[0] >= 25 and c[1] >= 15)]
        if not cells or l['name'].lower().replace('the ', '') in lm_names or l['kingdom'] == 'Crownhaven':
            continue
        mx = sum(c[0] for c in cells) / len(cells) + 0.5
        my = sum(c[1] for c in cells) / len(cells) + 0.5
        place_label(d, LB, l['name'], fR, *P(mx, my), 16, (92, 52, 28),
                    [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 2), (0, -2)],
                    halo=(244, 234, 206), hw=3)

    # --- the Antumbra inset
    draw_antumbra_inset(img, F, S)
    d = ImageDraw.Draw(img, 'RGBA')
    # compass rose in the western sea
    draw_compass(d, P(1.0, 16.6), 62)
    # scale bar
    fS = font(F_SERIF_I, 18)
    x0, y0 = P(0.5, 19.4)
    for k in range(4):
        d.rectangle([x0 + k * 40, y0, x0 + (k + 1) * 40, y0 + 8], fill=INK if k % 2 == 0 else (240, 230, 200),
                    outline=INK)
    d.text((x0, y0 - 6), "0", font=fS, fill=INK, anchor='mb')
    d.text((x0 + 160, y0 - 6), "12 leagues", font=fS, fill=INK, anchor='mb')

    # --- frame + bottom panel
    img = frame_and_panel(img.convert('RGB'))
    img.save(out_path, optimize=True)
    print('wrote', out_path, img.size)


def place_label(d, LB, txt, f, cx, cy, off, fill, dirs, halo=(244, 234, 206), hw=3):
    tb = d.textbbox((0, 0), txt, font=f, anchor='mm')
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    for dx, dy in dirs:
        x = cx + dx * (off + tw / 2 if dx else 0)
        y = cy + dy * (off + th / 2 if dy else 0)
        box = (x - tw / 2, y - th / 2 - 2, x + tw / 2, y + th / 2 + 2)
        if LB.free(box):
            d.text((x, y), txt, font=f, fill=fill, anchor='mm', stroke_width=hw, stroke_fill=halo)
            LB.add(box)
            return True
    # last resort: smaller offset scan around
    for rr in (1.6, 2.2, 2.8):
        for a in range(0, 360, 30):
            x = cx + math.cos(math.radians(a)) * off * rr + (tw / 2) * math.cos(math.radians(a))
            y = cy + math.sin(math.radians(a)) * off * rr
            box = (x - tw / 2, y - th / 2 - 2, x + tw / 2, y + th / 2 + 2)
            if LB.free(box):
                d.text((x, y), txt, font=f, fill=fill, anchor='mm', stroke_width=hw, stroke_fill=halo)
                LB.add(box)
                return True
    if f.size > 14:
        return place_label(d, LB, txt, font(f.path, f.size - 3), cx, cy, off, fill, dirs, halo, hw)
    print('  label dropped:', txt)
    return False


def rot_box(xy, txt, f, angle):
    tmp = Image.new('RGBA', (1, 1))
    tb = ImageDraw.Draw(tmp).textbbox((0, 0), txt, font=f, stroke_width=3)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    a = math.radians(angle)
    bw = abs(tw * math.cos(a)) + abs(th * math.sin(a))
    bh = abs(tw * math.sin(a)) + abs(th * math.cos(a))
    return (xy[0] - bw / 2, xy[1] - bh / 2, xy[0] + bw / 2, xy[1] + bh / 2)


def draw_rot_text(img, xy, txt, f, fill, angle, halo=None):
    tmp = Image.new('RGBA', (1, 1))
    tb = ImageDraw.Draw(tmp).textbbox((0, 0), txt, font=f, stroke_width=3)
    tw, th = tb[2] - tb[0] + 12, tb[3] - tb[1] + 12
    lay = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.text((tw / 2, th / 2), txt, font=f, fill=fill, anchor='mm', stroke_width=3 if halo else 0,
            stroke_fill=halo if halo else None)
    if angle:
        lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(lay, (int(xy[0] - lay.width / 2), int(xy[1] - lay.height / 2)))


def draw_tree(d, x, y, kind, zone):
    if kind in ('rime', 'pine'):
        dark = (44, 74, 70, 255) if kind == 'pine' else (90, 120, 120, 255)
        snow = (240, 246, 248, 255)
        d.polygon([(x, y - 13), (x - 6, y - 3), (x + 6, y - 3)], fill=dark, outline=(30, 44, 44, 255))
        d.polygon([(x, y - 8), (x - 7, y + 3), (x + 7, y + 3)], fill=dark, outline=(30, 44, 44, 255))
        d.line([(x, y - 13), (x - 3, y - 8)], fill=snow, width=2)
        if kind == 'rime':
            d.line([(x - 5, y - 1), (x - 1, y - 6)], fill=snow, width=2)
        d.line([(x, y + 3), (x, y + 6)], fill=(70, 50, 36, 255), width=2)
        return
    if kind == 'ash':
        d.line([(x, y + 6), (x, y - 4)], fill=(60, 52, 48, 255), width=2)
        d.ellipse([x - 6, y - 12, x + 6, y - 1], fill=(120, 108, 100, 255), outline=(60, 50, 44, 255))
        d.point([(x - 2, y - 8), (x + 3, y - 5), (x, y - 10)], fill=(255, 120, 40, 255))
        return
    if kind == 'petrified':
        d.line([(x, y + 6), (x, y - 8)], fill=(90, 84, 82, 255), width=3)
        d.line([(x, y - 3), (x - 5, y - 9)], fill=(90, 84, 82, 255), width=2)
        d.line([(x, y - 5), (x + 5, y - 10)], fill=(90, 84, 82, 255), width=2)
        return
    if kind == 'glass':
        d.polygon([(x, y - 12), (x - 5, y + 4), (x + 5, y + 4)], fill=(200, 214, 230, 255), outline=(90, 100, 130, 255))
        d.line([(x, y - 12), (x + 1, y + 3)], fill=(255, 255, 255, 255), width=1)
        return
    if kind == 'fungus':
        d.line([(x, y + 5), (x, y - 3)], fill=(220, 210, 190, 255), width=3)
        d.pieslice([x - 7, y - 9, x + 7, y + 1], 180, 360, fill=(170, 120, 190, 255), outline=(80, 50, 90, 255))
        d.point([(x - 2, y - 6), (x + 3, y - 5)], fill=(240, 255, 200, 255))
        return
    pal = {'broad': ((66, 108, 52), (98, 140, 70), (40, 70, 36)),
           'silk': ((112, 150, 104), (190, 214, 190), (60, 92, 64)),
           'gloam': ((70, 76, 96), (118, 110, 150), (40, 40, 60)),
           'wired': ((76, 112, 70), (120, 150, 90), (44, 66, 40))}.get(kind, ((66, 108, 52), (98, 140, 70), (40, 70, 36)))
    base, hi, ol = pal
    d.line([(x, y + 6), (x, y)], fill=(84, 60, 40, 255), width=2)
    d.ellipse([x - 7, y - 12, x + 7, y + 2], fill=base + (255,), outline=ol + (255,))
    d.ellipse([x - 4, y - 10, x + 2, y - 4], fill=hi + (255,))
    if kind == 'silk':
        d.arc([x - 9, y - 10, x + 9, y + 6], 200, 300, fill=(250, 250, 255, 220), width=1)
    if kind == 'gloam':
        d.point([(x + 3, y - 3)], fill=(255, 220, 120, 255))
    if kind == 'wired' and RNG.random() < 0.18:
        d.line([(x + 8, y + 6), (x + 8, y - 14)], fill=(110, 96, 70, 255), width=2)
        d.line([(x + 4, y - 11), (x + 12, y - 11)], fill=(110, 96, 70, 255), width=2)


def draw_peak(d, x, y, hgt, zone):
    hh = int(16 + 16 * hgt)
    ww = int(hh * 0.85)
    ks = kingdoms_of(zone)
    if 'Ashkaar' in ks:
        lit, sh = (128, 104, 92), (70, 56, 52)
    elif 'Ossaria' in ks:
        lit, sh = (214, 168, 112), (160, 110, 70)
    elif 'Crownhaven' in ks:
        lit, sh = (220, 210, 186), (150, 140, 120)
    else:
        lit, sh = (170, 160, 146), (110, 102, 96)
    top = (x, y - hh)
    d.polygon([top, (x - ww, y), (x, y)], fill=lit + (255,))
    d.polygon([top, (x + ww, y), (x, y)], fill=sh + (255,))
    d.line([(x - ww, y), top, (x + ww, y)], fill=INK + (255,), width=2)
    if hgt > 0.75 and 'Ashkaar' not in ks and 'Ossaria' not in ks:
        sw = ww * 0.38
        d.polygon([top, (x - sw, y - hh * 0.6), (x - sw * 0.3, y - hh * 0.66), (x, y - hh * 0.55),
                   (x + sw, y - hh * 0.6)], fill=(250, 250, 252, 255), outline=INK + (255,))


def draw_volcano(d, x, y):
    for k in range(5):
        r = 10 + k * 7
        d.ellipse([x - r * 0.6 + k * 6, y - 70 - k * 16 - r * 0.4, x + r * 0.6 + k * 6, y - 70 - k * 16 + r * 0.4],
                  fill=(90, 84, 82, 110 - k * 18))
    d.polygon([(x - 34, y - 58), (x - 70, y + 8), (x, y + 8)], fill=(118, 96, 86, 255))
    d.polygon([(x + 34, y - 58), (x + 70, y + 8), (x, y + 8), (x - 34, y - 58)], fill=(72, 58, 54, 255))
    d.polygon([(x - 34, y - 58), (x + 34, y - 58), (x + 70, y + 8), (x - 70, y + 8)], outline=INK + (255,))
    d.ellipse([x - 32, y - 64, x + 32, y - 52], fill=(230, 90, 30, 255), outline=INK + (255,))
    d.line([(x - 8, y - 54), (x - 20, y - 20), (x - 14, y + 4)], fill=(240, 110, 40, 255), width=4)
    d.line([(x + 12, y - 54), (x + 26, y - 14)], fill=(240, 110, 40, 255), width=3)


def draw_swords(d, x, y, s, col=(150, 26, 20, 255), ink=(40, 20, 16, 255)):
    for sgn in (-1, 1):
        d.line([(x - s * sgn, y - s), (x + s * sgn, y + s)], fill=ink, width=7)
        d.line([(x - s * sgn, y - s), (x + s * sgn, y + s)], fill=(236, 230, 220, 255), width=3)
        d.line([(x + s * sgn * 0.45 - s * 0.35, y + s * 0.45 + s * 0.35 * sgn),
                (x + s * sgn * 0.45 + s * 0.35, y + s * 0.45 - s * 0.35 * sgn)], fill=col, width=5)


def draw_war_big(d, P, S):
    war = G.WAR
    for key, c in (('isenmar', (40, 70, 130, 230)), ('ashkaar', (170, 40, 30, 230))):
        line = catmull(war[key], 10)
        for i in range(0, len(line) - 1, 2):
            d.line([P(*line[i]), P(*line[i + 1])], fill=c, width=4)
        (x1, y1), (x2, y2) = line[-2], line[-1]           # arrowhead at the front
        a = math.atan2(y2 - y1, x2 - x1)
        tip = P(x2, y2)
        d.polygon([tip, (tip[0] - 22 * math.cos(a - 0.45), tip[1] - 22 * math.sin(a - 0.45)),
                   (tip[0] - 22 * math.cos(a + 0.45), tip[1] - 22 * math.sin(a + 0.45))], fill=c)
    fr = catmull(war['front'], 8)
    d.line([P(*p) for p in fr], fill=(120, 20, 16, 240), width=9, joint='curve')
    d.line([P(*p) for p in fr], fill=(240, 160, 90, 255), width=3, joint='curve')
    bx, by = P(*war['battlefield'])
    d.ellipse([bx - 26, by - 26, bx + 26, by + 26], fill=(244, 236, 210, 200), outline=(120, 20, 16, 255), width=3)
    draw_swords(d, bx, by, 15)
    for key, (x, y) in war['camps'].items():
        px, py = P(x, y)
        c = (40, 70, 130, 255) if key == 'isenmar' else (170, 40, 30, 255)
        d.line([(px + 16, py - 4), (px + 16, py - 40)], fill=INK + (255,), width=3)
        d.polygon([(px + 17, py - 40), (px + 40, py - 33), (px + 17, py - 26)], fill=c, outline=INK + (255,))


def draw_gate(d, x, y, letter):
    d.ellipse([x - 13, y - 17, x + 13, y + 17], fill=(200, 210, 230, 255), outline=(60, 40, 90, 255), width=3)
    d.ellipse([x - 7, y - 11, x + 7, y + 11], fill=(120, 100, 170, 255))
    f = font(F_SERIF_B, 16)
    d.text((x, y), letter, font=f, fill=(250, 248, 255), anchor='mm')


def draw_town(d, x, y, rank, k):
    ban = BANNER.get(k.split('/')[0], (120, 100, 80))
    ban2 = BANNER.get(k.split('/')[-1], ban)
    if rank == 'seat':
        d.rectangle([x - 18, y - 10, x + 18, y + 12], fill=(232, 222, 200, 255), outline=INK + (255,), width=2)
        for tx in (-18, 0, 18):
            d.rectangle([x + tx - 6, y - 20, x + tx + 6, y + 12], fill=(240, 232, 212, 255), outline=INK + (255,), width=2)
            for bx in (-6, -1, 4):
                d.rectangle([x + tx + bx, y - 24, x + tx + bx + 2, y - 20], fill=INK + (255,))
        d.line([(x, y - 24), (x, y - 38)], fill=INK + (255,), width=2)
        d.polygon([(x, y - 38), (x + 14, y - 34), (x, y - 30)], fill=ban + (255,), outline=INK + (255,))
        d.rectangle([x - 4, y + 2, x + 4, y + 12], fill=INK + (255,))
        return (x - 26, y - 40, x + 26, y + 14)
    if rank in ('city', 'fort'):
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(236, 226, 204, 255), outline=INK + (255,), width=3)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=ban + (255,), outline=INK + (255,), width=2)
        if rank == 'fort':
            d.rectangle([x - 4, y - 4, x + 4, y + 4], fill=INK + (255,))
        return (x - 18, y - 18, x + 18, y + 18)
    if rank == 'town':
        d.rectangle([x - 11, y - 11, x + 11, y + 11], fill=(236, 226, 204, 255), outline=INK + (255,), width=3)
        d.polygon([(x - 7, y + 7), (x - 7, y - 7), (x + 7, y - 7)], fill=ban + (255,))
        d.polygon([(x + 7, y - 7), (x + 7, y + 7), (x - 7, y + 7)], fill=ban2 + (255,))
        return (x - 13, y - 13, x + 13, y + 13)
    d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(236, 226, 204, 255), outline=INK + (255,), width=3)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=ban + (255,))
    return (x - 12, y - 12, x + 12, y + 12)


def draw_gym_badge(d, x, y, n, f):
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(178, 40, 36, 255), outline=(250, 236, 200, 255), width=2)
    d.text((x, y + 1), str(n), font=f, fill=(255, 248, 230), anchor='mm')


def draw_road_shield(d, x, y, n, f):
    pts = [(x - 13, y - 13), (x + 13, y - 13), (x + 13, y + 3), (x, y + 15), (x - 13, y + 3)]
    d.polygon(pts, fill=(250, 240, 210, 255), outline=(92, 52, 28, 255))
    d.line(pts + [pts[0]], fill=(92, 52, 28, 255), width=2)
    d.text((x, y - 1), str(n), font=f, fill=(92, 52, 28), anchor='mm')


def draw_compass(d, c, r):
    x, y = c
    d.ellipse([x - r, y - r, x + r, y + r], outline=INK + (200,), width=2)
    d.ellipse([x - r * 0.8, y - r * 0.8, x + r * 0.8, y + r * 0.8], outline=INK + (140,), width=1)
    for a in range(0, 360, 45):
        L = r * (1.0 if a % 90 == 0 else 0.6)
        ax, ay = math.sin(math.radians(a)), -math.cos(math.radians(a))
        px, py = math.cos(math.radians(a)), math.sin(math.radians(a))
        tip = (x + ax * L, y + ay * L)
        l1 = (x + px * r * 0.14, y + py * r * 0.14)
        l2 = (x - px * r * 0.14, y - py * r * 0.14)
        d.polygon([tip, l1, (x, y)], fill=INK + (255,))
        d.polygon([tip, l2, (x, y)], fill=(240, 228, 196, 255), outline=INK + (255,))
    f = font(F_TITLE, 30)
    d.text((x, y - r - 18), 'N', font=f, fill=INK, anchor='mm', stroke_width=2, stroke_fill=(240, 228, 196))


def draw_antumbra_inset(img, F, S):
    x0, y0, x1, y1 = W.ANTUMBRA_INSET
    bx0, by0, bx1, by1 = int(x0 * S + 6), int(y0 * S + 6), int((x1 + 1) * S - 6), int((y1 + 1) * S - 6)
    w, h = bx1 - bx0, by1 - by0
    n = fnoise(w, h, 4, 91, 5)
    n2 = fnoise(w, h, 9, 92, 4)
    base = np.zeros((h, w, 3), np.float32)
    c1, c2 = np.array((66, 54, 96), np.float32), np.array((118, 98, 150), np.float32)
    base[:] = c1 * (1 - n[..., None]) + c2 * n[..., None]
    streak = (np.abs(((np.mgrid[0:h, 0:w][1] + np.mgrid[0:h, 0:w][0]) / 18.0 + n2 * 2) % 1.0 - 0.5) < 0.04)
    base[streak] = base[streak] * 0.6 + 220 * 0.4
    panel = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
    pd = ImageDraw.Draw(panel, 'RGBA')
    # inverted desert hanging in the sky: upside-down dunes along the top
    for k in range(9):
        cx = 20 + k * 44
        pd.arc([cx - 24, -10, cx + 24, 22], 20, 160, fill=(214, 190, 150, 160), width=3)
    off = lambda gx, gy: ((gx - x0) * S - 6, (gy - y0) * S - 6)
    # roads in the inset
    for nn, style, pts in road_polylines():
        if style != 'inset':
            continue
        line = [off(*p) for p in catmull(pts, 12)]
        pd.line(line, fill=(20, 12, 34, 255), width=10, joint='curve')
        pd.line(line, fill=(206, 196, 236, 255), width=6, joint='curve')
    fl = font(F_SERIF_I, 16)
    fT = font(F_SERIF_B, 22)
    for i, (nm, gx, gy, r, k) in W.SETTLEMENTS.items():
        if k != 'Antumbra':
            continue
        x, y = off(gx + 0.5, gy + 0.5)
        pd.rectangle([x - 14, y - 14, x + 14, y + 14], fill=(30, 20, 46, 255), outline=(230, 220, 255, 255), width=3)
        pd.polygon([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)], fill=(200, 180, 255, 255))
        txt = nm.upper() if r == 'seat' else nm
        pd.text((x, y + 30), txt, font=fT, fill=(250, 246, 255), anchor='mm', stroke_width=3, stroke_fill=(30, 20, 46))
    for g, (real, inset, nm) in W.GATES.items():
        x, y = off(*cell_center(inset))
        draw_gate(pd, x, y, g)
    placed = []
    for r, l in W.all_legs():
        if l['kingdom'] != 'Antumbra':
            continue
        cells = l['cells']
        mx = sum(c[0] for c in cells) / len(cells) + 0.5
        my = sum(c[1] for c in cells) / len(cells) + 0.5
        x, y = off(mx, my)
        y += -22
        pd.text((x, y), l['name'], font=fl, fill=(236, 226, 255), anchor='mm', stroke_width=3, stroke_fill=(30, 20, 46))
    # title
    ft = font(F_CAPS, 34)
    pd.text((w / 2, 34), spaced('ANTUMBRA', 1), font=ft, fill=(246, 240, 255), anchor='mm', stroke_width=3,
            stroke_fill=(30, 20, 46))
    pd.text((w / 2, 64), 'the Kingdom Behind the Glass', font=font(F_SERIF_I, 20), fill=(230, 220, 250), anchor='mm',
            stroke_width=2, stroke_fill=(30, 20, 46))
    pd.text((w / 2, h - 18), 'reached only through gates A, B and C', font=font(F_SERIF_I, 17), fill=(220, 210, 245),
            anchor='mm', stroke_width=2, stroke_fill=(30, 20, 46))
    # mirror frame
    fr = Image.new('RGBA', (w + 28, h + 28), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fr)
    fd.rounded_rectangle([0, 0, w + 27, h + 27], 16, fill=(196, 178, 120, 255), outline=INK + (255,), width=3)
    fd.rounded_rectangle([7, 7, w + 20, h + 20], 12, fill=(150, 126, 70, 255), outline=(250, 236, 180, 255), width=2)
    fr.alpha_composite(panel, (14, 14))
    sh = Image.new('RGBA', fr.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([0, 0, fr.width - 1, fr.height - 1], 16, fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(sh, (bx0 - 8, by0 - 6))
    img.alpha_composite(fr, (bx0 - 14, by0 - 14))


def frame_and_panel(img):
    w, h = img.size
    B = 40
    PH = 270
    out = Image.new('RGB', (w + 2 * B, h + 2 * B + PH), PARCH)
    pn = fnoise(out.width, out.height, 6, 71, 6)
    pa = np.asarray(out).astype(np.float32) * (0.9 + 0.12 * pn[..., None])
    out = Image.fromarray(np.clip(pa, 0, 255).astype(np.uint8))
    out.paste(img, (B, B))
    d = ImageDraw.Draw(out)
    d.rectangle([B - 3, B - 3, B + w + 2, B + h + 2], outline=INK, width=3)
    d.rectangle([B - 12, B - 12, B + w + 11, B + h + 11], outline=INK, width=2)
    d.rectangle([6, 6, out.width - 7, out.height - 7], outline=INK, width=3)
    for k in range(0, w + 24, 24):     # border tick pattern
        d.rectangle([B - 12 + k, B - 12, B - 12 + k + 11, B - 4], fill=INK)
    py = B + h + 26
    # title cartouche
    d.text((B + 30, py + 4), spaced('VELMORA', 1), font=font(F_CAPS, 84), fill=(70, 34, 22), anchor='la')
    d.text((B + 36, py + 118), 'The Seven Kingdoms and the Crown', font=font(F_SERIF_I, 32), fill=INK, anchor='la')
    d.text((B + 36, py + 160), 'The region of Pokemon Prismfall, three hundred years after the Glassfall', font=font(F_SERIF_I, 21),
           fill=(96, 70, 50), anchor='la')
    # legend
    lx = B + 790
    f = font(F_SERIF, 21)
    fb = font(F_SERIF_B, 22)
    d.text((lx, py + 6), 'Legend', font=fb, fill=INK, anchor='la')
    rows = [('seat', 'Kingdom seat (castle city)'), ('city', 'City'), ('town', 'Borderland town'), ('village', 'Village'),
            ('gym', 'Gym, in badge order'), ('shield', 'One of the Eighteen Roads (+ the Pilgrim Road)')]
    dd = ImageDraw.Draw(out, 'RGBA')
    for i, (k, t) in enumerate(rows):
        yy = py + 62 + i * 34
        if k == 'gym':
            draw_gym_badge(dd, lx + 16, yy, 3, font(F_SERIF_B, 15))
        elif k == 'shield':
            draw_road_shield(dd, lx + 16, yy, 7, font(F_SERIF_BI, 16))
        else:
            sc = {'seat': 0.6}.get(k, 0.8)
            draw_town(dd, lx + 16, yy + (6 if k == 'seat' else 0), k, 'Elowen')
        d.text((lx + 44, yy), t, font=f, fill=INK, anchor='lm')
    lx2 = lx + 500
    rows2 = [('road', 'Road (each named stretch is one or more maps)'), ('under', 'Underground road (the Blindwater)'),
             ('sea', 'Sea lane / ferry'), ('war', 'The war in the sands: marches and front'),
             ('air', 'Airship lane (the Mast Road, Act III)'), ('border', 'Kingdom border (mottled land = borderland)'),
             ('gate', 'Gate into Antumbra')]
    for i, (k, t) in enumerate(rows2):
        yy = py + 22 + i * 33
        if k == 'road':
            dd.line([(lx2, yy), (lx2 + 34, yy)], fill=(60, 40, 22), width=11)
            dd.line([(lx2, yy), (lx2 + 34, yy)], fill=(236, 214, 160), width=7)
        elif k in ('under', 'sea', 'war', 'air', 'border'):
            c = {'under': (60, 44, 30), 'sea': (40, 60, 90), 'war': (170, 40, 30), 'air': (120, 130, 150),
                 'border': (140, 50, 50)}[k]
            for s in range(0, 34, 9):
                dd.line([(lx2 + s, yy), (lx2 + s + 5, yy)], fill=c, width=4)
        elif k == 'gate':
            draw_gate(dd, lx2 + 16, yy, 'A')
        d.text((lx2 + 46, yy), t, font=f, fill=INK, anchor='lm')
    # gym order
    gx0 = lx2 + 540
    d.text((gx0, py + 6), 'The road of eighteen badges', font=fb, fill=INK, anchor='la')
    fs = font(F_SERIF, 17)
    for i, tid in enumerate(W.GYMS):
        col_ = i // 6
        row = i % 6
        nm = W.SETTLEMENTS[tid][0]
        d.text((gx0 + col_ * 175, py + 48 + row * 30), '%d  %s' % (i + 1, nm), font=fs, fill=INK, anchor='la')
    d.text((gx0, py + 48 + 6 * 30 + 4), 'then the Pilgrim Road to the Festival in Crownhaven, at the heart of the Crown Road',
           font=font(F_SERIF_I, 17), fill=(96, 70, 50), anchor='la')
    return out


# ----------------------------------------------------------------------------- the in-game Town Map (pixel art)
TM_PAL = {
    'Elowen': [(72, 136, 64), (96, 160, 76), (52, 104, 52)],
    'Isenmar': [(220, 232, 240), (196, 212, 228), (168, 188, 208)],
    'Zenith': [(200, 180, 132), (220, 200, 148), (168, 148, 108)],
    'Nadir': [(108, 116, 80), (128, 132, 92), (84, 92, 64)],
    'Ossaria': [(232, 196, 128), (244, 216, 152), (204, 152, 96)],
    'Ashkaar': [(112, 84, 76), (136, 100, 88), (84, 64, 60)],
    'Crownhaven': [(236, 224, 176), (248, 240, 200), (208, 192, 148)],
    'Antumbra': [(84, 68, 120), (104, 88, 144), (64, 52, 96)],
}


def paint_town_map(out_path):
    S = 16
    F = Fields(S)
    w, h = F.w, F.h
    img = np.zeros((h, w, 3), np.uint8)
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
    by = bayer[np.mgrid[0:h, 0:w][0] % 4, np.mgrid[0:h, 0:w][1] % 4]
    # sea
    dl = F.dist_land
    sea_cols = [(104, 176, 216), (80, 152, 200), (64, 128, 184)]
    lvl = np.clip((dl / 1.2 + (by - 0.5) * 0.35) * 2, 0, 2).astype(int)
    for i, c in enumerate(sea_cols):
        img[F.sea & (lvl == i)] = c
    img[F.frozen] = (216, 232, 240)
    img[F.frozen & (by > 0.85)] = (184, 208, 224)
    img[F.shattered & (fnoise(w, h, 30, 53, 2) > 0.56)] = (232, 240, 248)
    # land by zone
    for li, lab in enumerate(F.labels):
        m = F.zone == li
        ks = kingdoms_of(lab)
        p1 = TM_PAL[ks[0]]
        p2 = TM_PAL[ks[-1]]
        t = F.mixn
        if len(ks) == 2:
            useb = (t + (by - 0.5) * 0.5) > 0.5
        else:
            useb = np.zeros_like(m)
        sh = np.clip(((F.elev - 0.3) * 2 + (by - 0.5) * 0.6), -1, 1)
        for pal, sel in ((p1, ~useb), (p2, useb)):
            mm = m & sel & F.land
            img[mm & (sh < -0.2)] = pal[0]
            img[mm & (sh >= -0.2) & (sh < 0.4)] = pal[0]
            img[mm & (sh >= 0.4)] = pal[2]
            hl = mm & (F.grain > 0.62) & (by > 0.5)
            img[hl] = pal[1]
    # biomes
    img[F.land & (F.marsh > 0.5) & (by > 0.5)] = (80, 100, 64)
    img[F.land & (F.obsid > 0.5)] = (48, 40, 56)
    img[F.land & (F.sulfur > 0.6) & (by > 0.7)] = (200, 184, 92)
    # plateau: lighter top, rim drawn later
    img[F.plateau & (by > 0.75)] = (226, 208, 160)
    for nm, m in F.lakes.items():
        img[m] = {'sulfur': (212, 196, 96), 'mirror': (200, 208, 224), 'salt': (200, 220, 220),
                  'frozen': (224, 236, 244)}[G.LAKES[nm]['kind']]
    # coast outline
    land = F.land
    edge = land & ~ndimage.binary_erosion(land)
    img[edge] = (56, 64, 56)
    shore = ~land & ndimage.binary_dilation(land) & ~F.frozen
    img[shore] = (176, 216, 232)
    # plateau rim
    pe = F.plateau & ~ndimage.binary_erosion(F.plateau)
    img[pe] = (112, 92, 64)
    pe2 = F.plateau & ~ndimage.binary_erosion(F.plateau, iterations=3) & ~pe
    img[pe2 & (by > 0.4)] = (176, 152, 112)
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    # pixel glyphs: trees, peaks, dunes (drawn before rivers and routes, which sit on top)
    keepm = np.zeros((h, w), bool)
    for n, style, pts in road_polylines():
        if style == 'inset':
            continue
        if style == 'ring':
            pts = ring_points(pts, 48)
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            for t in np.linspace(0, 1, 40):
                px_, py_ = int((x1 + (x2 - x1) * t) * S), int((y1 + (y2 - y1) * t) * S)
                keepm[max(0, py_ - 4):py_ + 5, max(0, px_ - 4):px_ + 5] = True
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        keepm[y * S - 2:(y + 1) * S + 2, x * S - 2:(x + 1) * S + 2] = True
    x0i, y0i, x1i, y1i = W.ANTUMBRA_INSET
    keepm[y0i * S - 4:, x0i * S - 4:] = True
    TREE = {'broad': ((40, 96, 44), (72, 136, 64), (28, 64, 32)), 'silk': ((128, 176, 128), (208, 232, 208), (60, 100, 64)),
            'gloam': ((76, 72, 112), (128, 116, 168), (44, 40, 72)), 'rime': ((72, 112, 120), (232, 240, 244), (40, 64, 72)),
            'pine': ((40, 88, 80), (216, 232, 236), (24, 52, 48)), 'ash': ((112, 100, 96), (232, 112, 48), (64, 56, 52)),
            'wired': ((56, 104, 56), (200, 176, 96), (32, 64, 36)), 'glass': ((184, 200, 232), (248, 252, 255), (96, 104, 144)),
            'fungus': ((152, 104, 176), (232, 248, 192), (80, 52, 96)), 'petrified': ((120, 112, 108), (160, 152, 148), (72, 68, 64))}
    for ty in range(2, h - 6, 5):
        for tx in range(2 + (ty // 5 % 2) * 2, w - 5, 5):
            if not F.land[ty + 3, tx + 2] or keepm[ty + 3, tx + 2] or F.forest[ty + 3, tx + 2] < 0.5:
                continue
            ki = F.forest_kind[ty + 3, tx + 2]
            kind = F.fkinds[ki] if ki >= 0 else 'broad'
            body, hi, ol = TREE.get(kind, TREE['broad'])
            if kind in ('rime', 'pine', 'glass'):
                d.polygon([(tx + 2, ty), (tx, ty + 4), (tx + 4, ty + 4)], fill=body, outline=ol)
                d.point([(tx + 2, ty)], fill=hi)
                d.point([(tx + 2, ty + 5)], fill=(88, 64, 40))
            else:
                d.rectangle([tx, ty + 1, tx + 4, ty + 3], fill=body)
                d.rectangle([tx + 1, ty, tx + 3, ty + 4], fill=body)
                d.point([(tx + 1, ty + 1)], fill=hi)
                d.line([(tx + 1, ty + 4), (tx + 3, ty + 4)], fill=ol)
                d.point([(tx + 2, ty + 5)], fill=(88, 64, 40))

    def peak(px_, py_, big, snow, pal):
        hh = 6 if big else 4
        lit, sh = pal
        d.polygon([(px_, py_ - hh), (px_ - hh, py_), (px_, py_)], fill=lit)
        d.polygon([(px_, py_ - hh), (px_ + hh, py_), (px_, py_)], fill=sh)
        d.line([(px_ - hh, py_), (px_, py_ - hh), (px_ + hh, py_)], fill=(56, 48, 44))
        if snow:
            d.polygon([(px_, py_ - hh), (px_ - 2, py_ - hh + 2), (px_ + 2, py_ - hh + 2)], fill=(248, 248, 252))
    for pts, hgt, wid in G.RIDGES:
        line = catmull(pts, 30)
        acc = 0
        for i in range(len(line) - 1):
            acc += math.hypot(line[i + 1][0] - line[i][0], line[i + 1][1] - line[i][1])
            if acc > 0.42:
                acc = 0
                px_, py_ = int(line[i][0] * S + RNG.integers(-2, 3)), int(line[i][1] * S + RNG.integers(-2, 3))
                if 0 <= px_ < w and 0 <= py_ < h and F.land[py_, px_] and not keepm[py_, px_]:
                    zk = kingdoms_of(F.zone_name(py_, px_))
                    pal = ((160, 140, 124), (104, 92, 84)) if 'Ashkaar' in zk else \
                        (((220, 172, 112), (168, 116, 72)) if 'Ossaria' in zk else ((176, 168, 160), (120, 112, 108)))
                    peak(px_, py_, hgt > 0.7, hgt > 0.75 and 'Ashkaar' not in zk and 'Ossaria' not in zk, pal)
    cx_, cy_ = G.CROWNWALL['c']
    for a in range(0, 360, 26):
        if abs(((a - G.CROWNWALL['gap_angle']) + 180) % 360 - 180) < 20:
            continue
        px_ = int((cx_ + G.CROWNWALL['r'] * math.cos(math.radians(a))) * S)
        py_ = int((cy_ + G.CROWNWALL['r'] * math.sin(math.radians(a))) * S) + 3
        if not keepm[py_, px_]:
            peak(px_, py_, True, True, ((216, 208, 192), (152, 144, 132)))
    vx_, vy_ = int(G.VOLCANO[0] * S), int(G.VOLCANO[1] * S) + 4
    d.polygon([(vx_ - 9, vy_), (vx_ - 3, vy_ - 9), (vx_ + 3, vy_ - 9), (vx_ + 9, vy_)], fill=(96, 72, 64), outline=(48, 36, 32))
    d.line([(vx_ - 3, vy_ - 9), (vx_ + 3, vy_ - 9)], fill=(248, 120, 40), width=2)
    d.line([(vx_ - 1, vy_ - 8), (vx_ - 3, vy_ - 2)], fill=(232, 96, 32))
    for ty in range(0, h - 4, 7):
        for tx in range((ty // 7 % 2) * 4, w - 6, 8):
            if F.land[ty, tx] and not keepm[ty, tx] and F.dunes[ty, tx] > 0.5:
                d.line([(tx, ty + 2), (tx + 2, ty), (tx + 4, ty + 2)], fill=(200, 152, 96))
    # rivers
    for nm, rv in G.RIVERS.items():
        line = [(x * S, y * S) for x, y in catmull(rv['pts'], 8)]
        d.line(line, fill=(80, 152, 200) if rv['kind'] == 'water' else (96, 220, 220), width=2)
    # routes: Essentials-style cream bars between square centres
    for n, style, pts in road_polylines():
        if style == 'inset':
            continue
        if style == 'ring':
            pts = ring_points(pts, 48)
        line = [(x * S, y * S) for x, y in pts]
        if style == 'air':
            for (x1, y1), (x2, y2) in zip(line[:-1], line[1:]):
                L = max(1, int(math.hypot(x2 - x1, y2 - y1) / 4))
                for k in range(0, L, 2):
                    a, b = k / L, (k + 1) / L
                    d.line([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a), (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)],
                           fill=(250, 250, 255), width=1)
            continue
        if style in ('under', 'sea'):
            for (x1, y1), (x2, y2) in zip(line[:-1], line[1:]):
                L = max(1, int(math.hypot(x2 - x1, y2 - y1) / 6))
                for k in range(0, L, 2):
                    a, b = k / L, (k + 1) / L
                    d.line([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a), (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)],
                           fill=(248, 240, 216) if style == 'sea' else (90, 72, 56), width=2)
            continue
        d.line(line, fill=(72, 56, 40), width=6, joint='curve')
        d.line(line, fill=(248, 236, 200), width=4, joint='curve')
    # the war in the sands: the front (red), the two hosts' flags and the battlefield's crossed swords
    if getattr(G, 'WAR', None):
        fr = [(x * S, y * S) for x, y in G.WAR['front']]
        for (x1, y1), (x2, y2) in zip(fr[:-1], fr[1:]):
            d.line([(x1, y1), (x2, y2)], fill=(168, 32, 24), width=2)
        for key, (x, y) in G.WAR['camps'].items():
            px, py = int(x * S) + 5, int(y * S) - 6
            d.line([(px, py), (px, py + 7)], fill=(40, 32, 28))
            d.rectangle([px + 1, py, px + 4, py + 2], fill=(64, 112, 176) if key == 'isenmar' else (192, 40, 30))
    # dungeons / landmarks
    for mid, c in W.OWN_SQUARE.items():
        if c[0] >= 25 and c[1] >= 15:
            continue
        x, y = int((c[0] + 0.5) * S), int((c[1] + 0.5) * S)
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=(56, 40, 36))
        d.point([(x - 1, y - 1)], fill=(200, 184, 160))
    # towns
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        if k == 'Antumbra':
            continue
        cx, cy = (x + 0.5) * S, (y + 0.5) * S
        ban = BANNER.get(k.split('/')[0])
        if r == 'seat':
            d.rectangle([cx - 6, cy - 6, cx + 5, cy + 5], fill=(248, 240, 216), outline=(40, 32, 28))
            d.rectangle([cx - 3, cy - 3, cx + 2, cy + 2], fill=ban)
            d.rectangle([cx - 7, cy - 7, cx + 6, cy + 6], outline=(40, 32, 28))
        elif r in ('city', 'fort'):
            d.rectangle([cx - 5, cy - 5, cx + 4, cy + 4], fill=(248, 240, 216), outline=(40, 32, 28))
            d.rectangle([cx - 2, cy - 2, cx + 1, cy + 1], fill=ban)
        else:
            d.rectangle([cx - 4, cy - 4, cx + 3, cy + 3], fill=(248, 240, 216), outline=(40, 32, 28))
            d.point([(cx - 1, cy - 1), (cx, cy - 1), (cx - 1, cy), (cx, cy)], fill=ban)
    for g, (real, inset, nm) in W.GATES.items():
        cx, cy = (real[0] + 0.5) * S, (real[1] + 0.5) * S
        d.ellipse([cx - 3, cy - 4, cx + 3, cy + 4], fill=(150, 130, 210), outline=(40, 30, 60))
    if getattr(G, 'WAR', None):         # crossed swords over the Glass Dunes (drawn last so nothing covers them)
        wbx, wby = int(G.WAR['battlefield'][0] * S), int(G.WAR['battlefield'][1] * S)
        for sx in (-1, 1):
            d.line([(wbx - 4 * sx, wby - 4), (wbx + 4 * sx, wby + 4)], fill=(40, 24, 20), width=3)
            d.line([(wbx - 4 * sx, wby - 4), (wbx + 4 * sx, wby + 4)], fill=(236, 232, 224), width=1)
        d.point([(wbx - 2, wby + 2), (wbx + 2, wby + 2)], fill=(192, 40, 30))
    # Antumbra inset
    x0, y0, x1, y1 = W.ANTUMBRA_INSET
    bx0, by0, bx1, by1 = x0 * S + 2, y0 * S + 2, (x1 + 1) * S - 3, (y1 + 1) * S - 3
    sub = np.zeros((by1 - by0, bx1 - bx0, 3), np.uint8)
    nn = fnoise(bx1 - bx0, by1 - by0, 4, 93, 4)
    bb = by[by0:by1, bx0:bx1]
    sub[:] = (72, 60, 108)
    sub[(nn + (bb - 0.5) * 0.4) > 0.55] = (96, 82, 140)
    sub[(nn + (bb - 0.5) * 0.4) < 0.3] = (56, 46, 86)
    im.paste(Image.fromarray(sub), (bx0, by0))
    d = ImageDraw.Draw(im)
    d.rectangle([bx0 - 2, by0 - 2, bx1 + 1, by1 + 1], outline=(208, 184, 112))
    d.rectangle([bx0 - 1, by0 - 1, bx1, by1], outline=(40, 32, 28))
    for n, style, pts in road_polylines():
        if style != 'inset':
            continue
        line = [(x * S, y * S) for x, y in pts]
        d.line(line, fill=(30, 22, 44), width=6)
        d.line(line, fill=(216, 204, 248), width=4)
    for i, (n, x, y, r, k) in W.SETTLEMENTS.items():
        if k != 'Antumbra':
            continue
        cx, cy = (x + 0.5) * S, (y + 0.5) * S
        d.rectangle([cx - 6, cy - 6, cx + 5, cy + 5], fill=(232, 224, 255), outline=(30, 22, 44))
        d.rectangle([cx - 3, cy - 3, cx + 2, cy + 2], fill=BANNER['Antumbra'])
    for g, (real, inset, nm) in W.GATES.items():
        cx, cy = (inset[0] + 0.5) * S, (inset[1] + 0.5) * S
        d.ellipse([cx - 3, cy - 4, cx + 3, cy + 4], fill=(200, 190, 240), outline=(30, 22, 44))
    for mid, c in W.OWN_SQUARE.items():
        if not (c[0] >= 25 and c[1] >= 15):
            continue
        x, y = (c[0] + 0.5) * S, (c[1] + 0.5) * S
        d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=(40, 30, 60), outline=(220, 210, 250))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path)
    # a 2x preview inside the UI background for review
    prev = Image.new('RGB', (512, 384), (40, 48, 64))
    prev.paste(im, (16, 32))
    prev.resize((1024, 768), Image.NEAREST).save(os.path.join(ROOT, 'art', 'previews', 'town_map_preview_2x.png'))
    print('wrote', out_path, im.size)


if __name__ == '__main__':
    if '--big-only' not in sys.argv:
        paint_town_map(os.path.join(ROOT, 'graphics', 'UI', 'Town Map', 'prismfall_velmora.png'))
    if '--town-only' not in sys.argv:
        paint_big(os.path.join(ROOT, 'art', 'previews', 'world_map.png'))
