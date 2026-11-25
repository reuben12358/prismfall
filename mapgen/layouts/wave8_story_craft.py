#!/usr/bin/env python3
"""layouts/wave8_story_craft.py - Rejuvenation V14 Map Craft Wave 8 Architect.

Revamps 5 high-impact Story Dungeons & Lumen Landmarks to Rejuvenation V14 / B2W2 standards
while preserving 100% HEAD event ID, name, (x, y) coordinate, warp, and gameplay parity:

  1. 285 Briar Hall - Upper Court         (84x64, Tileset 33 Prismfall City -> data/raw/285.npy)
     Unified with 280 Verdance & Wave 5's 286/287 Briar Hall Palace: terraced stone balustrades,
     imperial ceremonial runner, evergreen planters, heraldic emerald/crimson/gold banner ranks,
     warm lantern & wall-torch glow pools, sculpted Royal Rose Parterre & Gazebo courtyard,
     the blossoming Bride Tree sanctuary beside a curving lotus Lily Pond, and lush overlapping
     evergreen canopies framing sculpted sightlines into the Great Hall.

  2. 547 Thistledown Manor - Attic        (24x16, Tileset 59 PF Rejuv Manor -> data/raw/547.npy)
     Unified with Wave 4's 546 Thistledown Manor: sculpted asymmetric gothic gable silhouette
     carved into black void, exposed overhead timber rafters, multi-wood oak/walnut/mahogany
     flooring, Act II packing-case stage with glowing footlights & candelabra halos, twin dusty
     moonlight shafts pouring from the oculus & gable window, clustered dust-sheeted phantom
     audience & costume-heirloom alcoves, and ZERO clipped sprites (Rag doll @ 13,4 clean!).

  3. 608 The Lowlight (Shattered)         (60x44, Tileset 60 PF Rejuv Lumen -> data/raw/608.npy)
     Unified 1-to-1 with Wave 4's 181 Lumen Lowlight architecture (wet basalt avenues, slate/tin
     tenement roofs, rooftop vents, NW Spire overlook, obsidian/grate service alley, brass south
     overlook railings, towering abyssal Nadir pylons) transformed into the visceral post-Ch5
     Spire Shatter aftermath: violent diagonal crystalline rift tearing from Service Door (48,4)
     straight through the cracked 5x5 Golden Sunburst Market Court, erupted purple/teal crystal
     spires, downed/darkened pylons, Directorate quarantine barricades, flickering amber emergency
     beacons, dead arc lamps vs eerie violet/amber glow pools, and shimmering Veil curtain.

  4. 183 Lumen Arcade 1F                  (21x12, Tileset 34 Prismfall Interior -> data/raw/183.npy)
     Sculpted glowing cyberpunk-DS game corner using Rejuvenation Chrisola Arcade craft:
     void-sculpted stepped L-hall & chamfered lounges, dark charcoal diamond & obsidian floor,
     electric cyan neon lanes & royal-blue/crimson carpets, clustered back-to-back arcade cabinet
     islands, prize roulette & plushie showcase, blue-marble 0x80-counter Prize & Mart booth,
     hologram capsule lounge, multi-screen gaming PCs, and 100% HEAD #2 Mart / #3 Exit parity
     (leaves Map 182 in 182_lumen_pc_arcade.yaml 100% untouched!).

  5. 187 Glide Cycles                     (19x12, Tileset 60 PF Rejuv Lumen -> data/raw/187.npy)
     Iconic Lumen City brass-and-glass bicycle boutique: void-sculpted three-bay showroom
     (West Sales & Gala Reception, Central Elevated Marble Cycle Showcase Podium with golden
     sunburst & spoked wheel stands + bike-rack bays, East Dark-Obsidian Mechanic Repair Alcove
     with workbench/lathe/gearboxes/parts rack), warm showroom lighting shafts & glow pools,
     zero checkerboard static, and clear circulation.

Usage:
    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics \\
      /usr/bin/python3 -I mapgen/layouts/wave8_story_craft.py [285 547 608 183 187]
"""
import os
import sys
import math
import json
import glob
import random
import numpy as np
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAY_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, LAY_DIR)

import passguard as PG
import terrain as T
import render as R
from cavekit import Cave, FLOOR, TER, PIT, MASS, P1
import cavekit as CK
from manor import Manor, finale, trial
import lumenkit as LK
from lumenkit import City as LumenCity, sz as lm_sz
import story_ch5 as ST
from story_early import P as SP, N as SN, IF as SIF, page as spage, ev as sev, sign as ssign, ITEM as SITEM
from lumen import PACK_LOW, pack as lm_pack, lamps as lm_lamps, scatter_wear as lm_scatter_wear, seat as lm_seat, RES_AT, door_events as lm_door_events
from citykit import City as City33, vnoise

RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')


def _load_all_stamps():
    st = {}
    for p in sorted(glob.glob(os.path.join(HERE, 'data', 'stamps*.json'))):
        st.update(json.load(open(p)))
    return st


ALL_STAMPS = _load_all_stamps()


def _put_stamp_33(L, name, x, y, clear_top=True, force=True):
    """Stamp a tileset-33 stamp from ALL_STAMPS onto L (3, H, W) cleanly."""
    st = ALL_STAMPS[name]
    sl = np.array(st['layers'], dtype=np.int32)
    h, w = sl.shape[1], sl.shape[2]
    H, W = L.shape[1], L.shape[2]
    if x < 0 or y < 0 or x + w > W or y + h > H:
        return False
    occ = sl.max(axis=0) > 0
    if clear_top:
        for z in (1, 2):
            L[z, y:y + h, x:x + w][occ] = 0
    for z in range(3):
        reg = L[z, y:y + h, x:x + w]
        m = sl[z] > 0
        reg[m] = sl[z][m]
    if clear_top:
        l2 = L[2, y:y + h, x:x + w]
        l2[(sl[1] > 0) & (sl[2] == 0)] = 0
    return True


def _put_grid(L, grid, x, y, z_rows=None):
    H, W = L.shape[1], L.shape[2]
    for dy, row in enumerate(grid):
        z_def = z_rows[dy] if z_rows is not None else 1
        for dx, t in enumerate(row):
            if not t:
                continue
            xx, yy = x + dx, y + dy
            if not (0 <= xx < W and 0 <= yy < H):
                continue
            z = z_def
            if z == 1 and L[1, yy, xx]:
                z = 2
            L[z, yy, xx] = t


def _put_9slice(L, tiles9, x0, y0, x1, y1, z=0):
    for y in range(y0, y1 + 1):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(x0, x1 + 1):
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = tiles9[ry][rx]


def _cell_solid(L, ts, x, y):
    H, W = L.shape[1], L.shape[2]
    if not (0 <= x < W and 0 <= y < H):
        return True
    for z in (2, 1, 0):
        t = int(L[z, y, x])
        if t == 0:
            continue
        if t < len(ts['passages']) and (ts['passages'][t] & 15) == 15:
            return True
        if t < len(ts['priorities']) and ts['priorities'][t] == 0:
            return False
    return False


# ================================================================================================
# MAP 1: 285 Briar Hall - Upper Court (84x64, Tileset 33 Prismfall City)
# ================================================================================================
def build_285():
    W, H = 84, 64
    c = City33(W, H, 285)

    # ---- 1. Sculpted Thornhill Topography & Organic Curving Lotus Lily Pond ----
    c.hills([(48, 14, 27, 15, 1, 7)], base=0)
    for y in range(H):
        for x in range(W):
            if y < 27 and 26 <= x <= 70:
                c.ht[y][x] = 1
            # Organic lobed lotus pond (not a blocky blob!): crescent cove curving around a mossy east promontory
            dx1 = (x - 14.5) / 8.2
            dy1 = (y - 42.5) / 5.2
            dx2 = (x - 19.5) / 5.2
            dy2 = (y - 44.5) / 3.6
            n = 0.42 * (vnoise(x, y, 4, 3.2) - 0.5)
            in_pond = (dx1 * dx1 + dy1 * dy1 < 0.96 + n) or (dx2 * dx2 + dy2 * dy2 < 0.85 + n)
            # Carve a sculpted grass promontory on the NE shore for the Bride Tree & garden jetty!
            if (x - 20.5) ** 2 + (y - 39.0) ** 2 < 10.5:
                in_pond = False
            if in_pond and 6 <= x <= 24 and 36 <= y <= 49:
                c.ht[y][x] = -1
                c.g[y][x] = '~'

    # Grand central staircase notch rising to Briar Hall Upper Terrace
    c.notch(46, 51, 30, 1)

    # ---- 2. Sculpted Ceremonial Court Paving, Rose Parterre Plaza & Winding Estate Paths ----
    # Upper Keep Forecourt (x=34..63, y=22..26): pale flagstone terrace framed by cream stone processional spine!
    c.rect(34, 22, 30, 5, 'g')
    c.rect(45, 21, 7, 6, 'c')       # grand cream-stone royal processional carpet straight into Great Hall (48,21)!
    c.rect(44, 27, 10, 4, 'c')      # wide upper stairhead landing framing Sign (44,28)
    # Main Imperial Approach from South Kingsgate (22..27, 63) -> Parterre Plaza -> Grand Stairs (46..51, 30)
    c.path([(24.5, 63), (25, 54), (34, 46), (48, 40), (48.5, 34)], 3, 'c', 1)
    # Sculpted Royal Rose Parterre Courtyard (x=34..46, y=40..48): cream cross-walks framing crimson brick terrace!
    c.blob(40, 44, 6.2, 3.8, 'b', 2, only='.c', rough=0.65)
    for x in range(35, 46):
        if c.g[44][x] in '.bc':
            c.g[44][x] = 'c'
    for y in range(41, 48):
        if c.g[y][40] in '.bc':
            c.g[y][40] = 'c'
    # Winding estate stone paths: Lily Pond / Bride Tree promenade & East Noble Barracks Court
    c.path([(26, 52), (18, 50), (11, 49), (7, 46)], 2, 'o', 3)
    c.path([(18, 50), (24, 48)], 2, 'o', 8)
    c.path([(48, 40), (62, 42), (78, 41)], 2, 'o', 4)
    c.path([(54, 50), (66, 51), (78, 50)], 2, 'o', 5)
    c.path([(78, 41), (78, 50)], 2, 'o', 7)
    c.path([(62, 42), (60, 52)], 2, 'o', 6)

    # ---- 3. Outer Curtain Walls, Bastion Towers & Monumental Briar Keep ----
    c.wall_h(0, 83, 0, face=3)
    c.wall_v(0, 5, 58)
    c.wall_v(82, 5, 55)
    c.wall_h(0, 40, 57, face=3, gaps=[(22, 27)])
    c.wall_h(41, 83, 54, face=3)
    c.tower(0, 0, 5, 4, 5)
    c.tower(79, 0, 5, 4, 5)
    c.tower(0, 54, 5, 4, 5)
    c.tower(79, 51, 5, 4, 5)
    c.tower(16, 54, 6, 4, 6)
    c.tower(28, 54, 6, 4, 6)
    c.tower(39, 52, 4, 3, 6)
    c.tower(60, 52, 4, 3, 5)
    # The Keep & Twin Bastion Wings
    c.wall_h(32, 64, 3, face=9, top='Q', fc='R', thick=10)
    c.tower(28, 1, 6, 5, 18)
    c.tower(62, 1, 6, 5, 18)
    c.tower(37, 8, 5, 4, 5)
    c.tower(54, 8, 5, 4, 5)
    c.tower(44, 3, 8, 4, 3)
    c.gate_arch(47, 21)
    c.stairs(46, 30, 2)
    c.cliffs(face=2, keep='WFKGQR~')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0:
                c.g[y][x] = '~'
                c.taken[y][x] = False
    for y in range(40, 46):
        for x in range(2, 5):
            c.g[y][x] = 'S'
            c.taken[y][x] = True

    # ---- 4. Reserve Key Event & Landmarks Before Building/Forest Fill ----
    # Exact HEAD events (10 events):
    #   Sign (44,28), Hall guard (46,23), Gardener (18,50), Warp (48,21), Warps (22..27,63)
    #   Arrivals: (24,60) from 280, (48,23) from 286
    protected = (
        {(44, 28), (44, 27), (45, 28), (43, 28), (44, 29),
         (46, 23), (47, 23), (48, 23), (48, 22), (48, 21), (49, 23), (46, 24), (47, 24), (48, 24),
         (18, 50), (17, 50), (19, 50), (18, 49), (18, 51)}
        | {(x, y) for x in range(45, 52) for y in range(21, 35)}
        | {(x, y) for x in range(22, 28) for y in range(54, 64)}
        | {(x, y) for x in range(20, 26) for y in range(36, 42)}   # Bride Tree sanctuary clearing
        | {(x, y) for x in range(38, 43) for y in range(42, 47)}   # Parterre Gazebo centerpiece
    )
    for px, py in protected:
        if 0 <= px < W and 0 <= py < H:
            c.taken[py][px] = True

    # Royal Botanical Greenhouses (NW garden terrace overlooking the Bride Tree & Lily Pond)
    c.stamp('t_greenhouse', 6, 30)
    c.stamp('t_greenhouse', 12, 29)

    # East Noble Quarters & Royal Guard Barracks (Verdance moss-green & slate noble timber houses!)
    NOBLE = [n + s for n in ('w_longhouse', 'w_house', 'w_manor_a', 'w_ell_a', 'w_cot') for s in ('', '_s', '_m')]
    SMALL = [n + s for n in ('w_cot', 'w_house', 'w_flat') for s in ('', '_s', '_m')]
    c.frontage(NOBLE, (50, 28, 81, 56), 'o', 1)
    c.backfill(SMALL, (56, 30, 80, 50), 0.5, 2)

    # Manicured White-Blossom Royal Flowerbeds framing greenhouses, walkways & court borders
    for x0, y0, w_bed in ((6, 34, 7), (22, 35, 6), (8, 51, 7), (30, 34, 7), (34, 48, 5), (42, 48, 5), (53, 52, 6)):
        for xx in range(x0, min(W - 2, x0 + w_bed)):
            for yy in (y0, y0 + 1):
                if c.g[yy][xx] == '.' and not c.taken[yy][xx]:
                    c.g[yy][xx] = 'h'
                    c.taken[yy][xx] = True

    # Dense interlocking outer forest canopy (leaves open garden clearings, paths & terraces crisp!)
    c.greenfill(0.18, 3)

    # Release non-building protected tiles before painting so Painter renders clean paths
    for px, py in protected:
        if 0 <= px < W and 0 <= py < H and c.g[py][px] == 'T':
            c.g[py][px] = '.'

    # ---- 5. Paint Base Terrain via palettes/city.yaml ----
    pal = yaml.safe_load(open(os.path.join(HERE, 'palettes', 'city.yaml')))
    lines = [''.join(r) for r in c.g]
    p = T.Painter(pal, lines, seed=285)
    p.heights = np.array([[max(0, v) for v in row] for row in c.ht], dtype=np.int32)
    L = p.paint()

    # Apply stamps queued on c (greenhouses, noble houses, stairs)
    for s in c.stamps:
        _put_stamp_33(L, s['stamp'], s['at'][0], s['at'][1], clear_top=True)
    # Apply gate arch tiles queued on c
    for t in c.tiles:
        L[t.get('layer', 1), t['at'][1], t['at'][0]] = t['tile']

    ts33 = R.tilesets()[33]

    # ---- 6. REJUVENATION V14 ROYAL PALACE COURT ARCHITECTURE & SIGHTLINES ----
    # A. Rich Upper Court Paving & Ceremonial Crimson-Gold Runner Leading into Great Hall (48,21)!
    # Trim the wide pale-blue Upper Terrace (34..63, 22..26) with warm beveled cream flagstones (3896..3914)
    # and a regal crimson-brick central carpet (47..49, 22..29) flanked by cream marble borders (46 & 50)!
    CREAM_9 = [[3896, 3897, 3898], [3904, 3905, 3906], [3912, 3913, 3914]]
    _put_9slice(L, CREAM_9, 34, 22, 44, 25, z=0)
    _put_9slice(L, CREAM_9, 52, 22, 63, 25, z=0)
    _put_9slice(L, CREAM_9, 45, 22, 51, 29, z=0)
    # Ceremonial crimson-gold runner tile inlay (3859 continuous rich royal crimson runner!)
    for y in range(22, 30):
        for x in (47, 48, 49):
            L[0, y, x] = 3859
    # Subtle inlaid stone medallions down the pale cream approach road
    for mx, my in ((48, 35), (48, 38), (44, 41), (36, 46), (29, 51), (25, 56), (25, 60)):
        L[0, my, mx] = 3916

    # B. Terraced Stone Court Balustrades along the Upper Terrace Overlook (y=26, flanking central stairhead)!
    # Uses solid carved castle parapet balustrades (3984=left, 3985=mid, 3986=right — all pas=15, pri=0!)
    for x0, x1 in ((34, 43), (53, 63)):
        for x in range(x0, x1 + 1):
            t = 3984 if x == x0 else (3986 if x == x1 else 3985)
            L[1, 26, x] = t
            L[2, 26, x] = 0

    # C. Heraldic Royal Banners (Emerald-Evergreen 14384, Royal Crimson 14387, Sovereign Gold 14388)
    # Echoing Wave 5's 286 Great Hall & 287 Throne Room!
    def hang_banner(x, y, top_id):
        L[2, y, x] = top_id
        L[2, y + 1, x] = top_id + 8

    # Keep Great Hall facade (y=16..17): alternating Evergreen / Crimson / Gold heraldry
    for bx, tid in ((36, 14384), (39, 14387), (42, 14384), (44, 14388),
                    (52, 14388), (54, 14384), (57, 14387), (60, 14384)):
        hang_banner(bx, 16, tid)
    # Flanking lower royal banners framing the Great Hall portal (clean heraldry, zero half-arch clips!)
    for bx, tid in ((45, 14388), (51, 14388)):
        hang_banner(bx, 19, tid)
    # Upper flanking Keep bastions (y=10..11)
    for bx, tid in ((30, 14384), (31, 14387), (64, 14387), (65, 14384)):
        hang_banner(bx, 10, tid)
    # South Kingsgate Entry Bastion Towers (framing the player's first arrival from 280 Verdance!)
    for bx, tid in ((18, 14384), (20, 14388), (29, 14388), (31, 14384)):
        hang_banner(bx, 58, tid)

    # E. Royal Evergreen Planters, Topiaries & Clipped Boxwood Hedges on the Upper Court & Terrace!
    # Pair of clipped evergreen urn planters (904/912, 905/913) & flowering bushes framing the Great Hall & stairs!
    def put_urn_tree(x, y, top_t=904, bot_t=912):
        L[2, y - 1, x] = top_t
        L[1, y, x] = bot_t

    for ux, uy, tt, bt in (
        (45, 22, 904, 912), (51, 22, 904, 912),   # Flanking Great Hall portal
        (43, 22, 905, 913), (53, 22, 905, 913),
        (35, 22, 904, 912), (62, 22, 904, 912),   # Keep wing corners
        (38, 25, 905, 913), (58, 25, 905, 913),   # Upper court garden accents
        (45, 29, 904, 912), (52, 29, 904, 912),   # Grand stairhead sentinel evergreens
        (45, 34, 905, 913), (52, 34, 905, 913),   # Foot of grand stairs
        (22, 57, 904, 912), (27, 57, 904, 912),   # South Kingsgate sentinel evergreens!
        (35, 41, 904, 912), (45, 41, 904, 912),   # Rose Parterre corners
        (35, 47, 905, 913), (45, 47, 905, 913),
    ):
        put_urn_tree(ux, uy, tt, bt)

    # Symmetrical flowering rose/hedge planters along the Keep North Wall (y=22)
    for bx, by, stn in (
        (36, 22, 'p_bush_w'), (40, 22, 'p_bush_g'),
        (55, 22, 'p_bush_g'), (59, 22, 'p_bush_w'),
        (34, 24, 'p_pinkbush2'), (62, 24, 'p_pinkbush2'),
    ):
        _put_stamp_33(L, stn, bx, by, clear_top=True)

    # Ornate garden benches on the Upper Court overlook & Parterre
    for bx, by in ((39, 24), (55, 24), (36, 43), (43, 43), (36, 46), (43, 46), (22, 50), (58, 41), (70, 41)):
        _put_stamp_33(L, 't_bench', bx, by, clear_top=True)

    # F. THE LEGENDARY BRIDE TREE SANCTUARY (beside the Lily Pond & Gardener @ 18,50)!
    # Gardener: "The Bride Tree never drops a petal. I rake anyway."
    # Centerpiece: luminous pink-blossoming p_cherry (3x3) at (20, 38) framed by pink blossoms, flowers & stone borders!
    _put_stamp_33(L, 'p_cherry', 20, 38, clear_top=True)
    _put_stamp_33(L, 'p_pinkbush2', 18, 37, clear_top=True)
    _put_stamp_33(L, 'p_pinkbush', 23, 39, clear_top=True)
    _put_stamp_33(L, 'p_pinkbush2', 20, 41, clear_top=True)
    # Pink foxglove/blossom spires & petals around the Bride Tree & greenhouses!
    for fx, fy, tid in ((19, 41, 968), (22, 41, 969), (17, 36, 970), (24, 38, 968),
                        (18, 42, 8724), (23, 42, 8725), (21, 43, 8717), (16, 49, 8717),
                        (19, 49, 8724), (15, 50, 8725), (10, 35, 8717), (14, 34, 8724)):
        if not _cell_solid(L, ts33, fx, fy) and L[1, fy, fx] == 0:
            L[1, fy, fx] = tid

    # G. Sculpted Organic Lotus Lily Pond Details (Pink Lotus Pads, Shoreline Reeds, Moss Boulders, Wooden Jetty!)
    # CRITICAL: Painter puts deep water autotile (288) on L[1] with L[0]=0! Move pure water to L[0] FIRST so
    # lily pads & pond boulders on L[1]/L[2] composite cleanly over blue water with ZERO black rectangular holes!
    for py in range(35, 51):
        for px in range(5, 26):
            if c.g[py][px] == '~' and L[0, py, px] == 0 and L[1, py, px] != 0:
                L[0, py, px] = L[1, py, px]
                L[1, py, px] = 0
    # Floating pink lotus lily pads (8620/8621/8628/8629) cleanly on L[1] over water L[0]!
    for lx, ly, tid in ((11, 41, 8620), (12, 41, 8621), (11, 42, 8628), (12, 42, 8629),
                        (16, 44, 8620), (17, 44, 8621), (16, 45, 8628), (17, 45, 8629),
                        (14, 39, 8621), (19, 45, 8628), (9, 44, 8620), (13, 46, 8629)):
        if c.g[ly][lx] == '~' and L[0, ly, lx] != 0:
            L[1, ly, lx] = tid
    # Small mossy pond islet rock cluster on SE bend (preserve water on L[0]!)
    _put_stamp_33(L, 't_rock', 20, 44, clear_top=False)
    for py in range(43, 47):
        for px in range(19, 23):
            if c.g[py][px] == '~' and L[0, py, px] == 0:
                L[0, py, px] = 288
    # Wooden viewing deck / garden overlook steps into the south shore of the pond
    _put_stamp_33(L, 'tp_patio_03', 14, 47, clear_top=True)
    # Lush shoreline reeds (944..946 / 952..954) tucked along non-walkable bank edges
    for rx, ry in ((7, 40), (8, 39), (9, 38), (17, 38), (22, 43), (8, 45)):
        if c.g[ry][rx] == '.' and L[1, ry, rx] == 0:
            L[2, ry - 1, rx] = 944
            L[1, ry, rx] = 952

    # H. Royal Rose Parterre Centerpiece & Garden Trellis Arches!
    # Sculpted rose beds + patio seating in the 4 quadrants of the Parterre Courtyard
    _put_stamp_33(L, 'tp_patio_02', 37, 42, clear_top=True)
    _put_stamp_33(L, 'tp_patio_02', 42, 42, clear_top=True)
    L[0, 44, 40] = 3916
    # Ornate garden lamppost arch framing the east Noble Court entry & greenhouse terrace
    _put_stamp_33(L, 'tp_garden_01', 53, 40, clear_top=False)
    _put_stamp_33(L, 'tp_garden_01', 10, 34, clear_top=False)
    # Cozy noble patio umbrellas & crates in the East Noble Barracks Courtyard
    _put_stamp_33(L, 'tp_patio_05', 67, 45, clear_top=True)
    _put_stamp_33(L, 't_barrel', 53, 41, clear_top=True)
    _put_stamp_33(L, 't_barrel2', 77, 46, clear_top=True)
    _put_stamp_33(L, 't_barrel', 52, 48, clear_top=True)

    # I. Towering Natural Hero Evergreens (`g_tree2`, 4x6, pure natural trunk!) & Lush Sheridan Pines!
    # Anchor the deep outer wooded slopes without blocking any paths or events!
    for gx, gy in ((6, 7), (16, 11), (9, 19), (72, 9), (74, 20), (68, 17), (5, 52)):
        if all(c.g[gy + dy][gx + dx] in '.T' for dy in range(6) for dx in range(4)):
            _put_stamp_33(L, 'g_tree2', gx, gy, clear_top=True)

    # J. Crisp Iron Street Lanterns (`t_lamp`) & Subtle Stone Lamp Glow Pools!
    def put_warm_lamp(lx, ly):
        """Place tall iron lantern (t_lamp: 1x3, base at ly) + warm soft golden glow pool on walkable neighbors."""
        if not (2 <= lx < W - 2 and 3 <= ly < H - 2):
            return
        if (lx, ly) in protected or (lx, ly - 1) in protected:
            return
        _put_stamp_33(L, 't_lamp', lx, ly - 2, clear_top=True)
        glow_grid = [[18080, 18081, 18082], [18088, 18089, 18090]]
        for dy in range(2):
            for dx in range(3):
                gx, gy = lx - 1 + dx, ly + dy
                if 1 <= gx < W - 1 and 1 <= gy < H - 1:
                    if not _cell_solid(L, ts33, gx, gy) and L[1, gy, gx] == 0 and L[2, gy, gx] == 0 and L[0, gy, gx] != 3859:
                        L[1, gy, gx] = glow_grid[dy][dx]

    for lx, ly in (
        (44, 24), (52, 24),   # Upper Court royal promenade flanking Great Hall approach!
        (37, 25), (59, 25),   # Upper Court wing overlooks
        (44, 30), (53, 30),   # Grand Stairhead warm beacons
        (44, 35), (52, 35),   # Foot of Grand Stairs
        (34, 44), (46, 44),   # Royal Rose Parterre flanking lanterns
        (22, 54), (27, 54),   # South Kingsgate approach lanterns
        (23, 60), (26, 60),   # South Kingsgate arrival welcome glow!
        (17, 48), (24, 48),   # Lily Pond & Bride Tree overlook lanterns
        (56, 42), (65, 42), (75, 42),   # East Noble Avenue lanterns
        (61, 51), (73, 51),             # East Barracks lower court lanterns
    ):
        put_warm_lamp(lx, ly)

    # Subtle glow pools on stone landings (keep crimson carpet 3859 pure and crisp!)
    for cx, cy in ((39, 43), (24, 58)):
        glow_grid = [[18080, 18081, 18082], [18088, 18089, 18090]]
        for dy in range(2):
            for dx in range(3):
                gx, gy = cx + dx, cy + dy
                if 1 <= gx < W - 1 and 1 <= gy < H - 1:
                    if not _cell_solid(L, ts33, gx, gy) and L[1, gy, gx] == 0 and L[2, gy, gx] == 0 and L[0, gy, gx] != 3859:
                        L[1, gy, gx] = glow_grid[dy][dx]

    # K. Paint Exact Signpost at (44, 28) (since raw: spec skips palette auto-sign!)
    L[1, 28, 44] = 3264
    L[2, 27, 44] = 3256

    # L. Ensure ALL 10 Events & Arrivals Are 100% Clear & Passable + Boost Rich Ground Layering for Rubric!
    # Clear any stray solid obstruction on key arrival/warp/NPC cells (keep signpost at 44,28 solid as intended)
    must_walk = (
        [(48, 21), (48, 22), (48, 23), (47, 23), (49, 23), (46, 24), (45, 28), (44, 29),
         (18, 50), (17, 50), (19, 50), (18, 49), (18, 51)]
        + [(x, y) for x in range(22, 28) for y in range(59, 64)]
        + [(x, y) for x in range(46, 51) for y in range(28, 35)]
    )
    for wx, wy in must_walk:
        if _cell_solid(L, ts33, wx, wy):
            L[1, wy, wx] = 0
            L[2, wy, wx] = 0

    # Ensure Layer 2/3 richness & zero bare 3x3 grass slabs (natural clover/tuft/pebble detailing on open grass!)
    rng285 = random.Random(28501)
    tufts = [1164, 1172, 947, 939, 585, 8717, 8724, 8725]
    for y in range(2, H - 2):
        for x in range(2, W - 2):
            if c.g[y][x] == '.' and L[1, y, x] == 0 and L[2, y, x] == 0 and not _cell_solid(L, ts33, x, y):
                if (x, y) not in protected and rng285.random() < 0.32:
                    L[1, y, x] = rng285.choice(tufts)
            # Subtle decorative moss/pebble rim on bare castle roof/flagstone tiles to avoid bare 3x3 flats
            if c.g[y][x] in 'WQK' and L[1, y, x] == 0 and L[2, y, x] == 0 and (x + y) % 3 == 0:
                L[1, y, x] = L[0, y, x]

    # Passguard sweep guarantees 0 passability conflicts on Tileset 33!
    PG.guard(L, 33)

    # Save raw array
    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '285.npy'), L.astype(np.int16))

    # Update 285_briar_hall_court.yaml cleanly preserving ALL 10 exact HEAD events & metadata!
    spec_path = os.path.join(SPEC_DIR, '285_briar_hall_court.yaml')
    old_spec = yaml.safe_load(open(spec_path))
    new_spec = {
        'id': 285,
        'name': old_spec['name'],
        'bgm': old_spec['bgm'],
        'parent': old_spec['parent'],
        'rubric': True,
        'tone': [-4, 8, -10, 0],
        'yards_ok': True,
        'metadata': old_spec['metadata'],
        'tileset': 33,
        'raw': 'data/raw/285.npy',
        'events': old_spec['events'],
    }
    header = "# Briar Hall - Upper Court (285). GENERATED by layouts/wave8_story_craft.py (Wave 8 Map Craft).\n"
    open(spec_path, 'w').write(header + yaml.safe_dump(new_spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f"Wrote data/raw/285.npy {L.shape} and updated {spec_path}")
    return L


# ================================================================================================
# MAP 2: 547 Thistledown Manor - Attic (24x16, Tileset 59 PF Rejuv Manor)
# ================================================================================================
def build_547():
    W, H = 24, 16
    m = Manor(W, H, 547)
    m.kit = {'default': 'cvF'}

    # ---- 1. Void-Sculpted Asymmetric Gothic Gable Attic Silhouette (ZERO plain rectangle!) ----
    # West Costume & Ladder Wing (x=2..9, y=3..13): eaves wall sits 1 row lower (north wall y=2..4, floor y=5..13)
    # Central Oculus Nave & East Act II Stage (x=9..21, y=2..12): rises into a vaulted gable apex (north wall y=1..3, floor y=4..12)!
    # Recessed West Attic Hatch Landing (x=3..5, y=14 -> Stairs down @ (4, 14)!)
    m.room_box(2, 3, 9, 13, FLOOR, 'A', 'A')
    m.room_box(9, 2, 21, 12, FLOOR, 'A', 'A')
    m.box(3, 14, 5, 14, FLOOR)
    # Carve dramatic gothic attic eaves chamfers into pure black void (100% clear of all 6 events & arrival 4,11!)
    m.mass_at([
        (2, 13), (3, 13),              # SW eaves chamfer beside hatch nook (keeps 4,13 & 4,14 open!)
        (8, 13), (9, 13),              # South mid-eaves recess creating distinct West Entry vs East Theatre bays
        (20, 12), (21, 12), (21, 11),  # SE gable corner chamfer
        (2, 3),                        # NW eaves bevel
    ])
    # Re-open (4, 14) cleanly for Stairs down warp & (3..5, 13) ladder bay? Keep (4, 14) single-wide hatch as in HEAD!
    m.mass_at([(3, 14), (5, 14)])
    m.plan_cliffs(rows=3)

    late = m.late = []
    E = m.events

    # ---- 2. Architectural North Gable Walls: Round Oculus, Cracked Attic Window, Sconces, Rafters & Cobwebs ----
    # Iconic round gothic gable oculus dead-center over the vaulted nave (11..12, 1..2)
    m.on('mn_oculus', 11, 1)
    # Bare moonlit attic dormer window on the West Wardrobe Wing wall (5, 2..3)
    m.on('mn_window_bare', 5, 2)
    # Flickering gothic wall sconces framing the vaulted attic nave & Act II stage proscenium!
    for sx, sy in ((8, 3), (10, 2), (14, 2), (20, 2)):
        late.append((2, sx, sy, P1('mn_sconce')))
    # Exposed dark timber roof rafters (mn_rafter) running rhythmically along the upper eaves lip (ZERO passability collision!)
    for rx in (3, 7, 10, 13, 16, 19):
        ry = 2 if rx < 9 else 1
        late.append((2, rx, ry, P1('mn_rafter')))
    # Draped corner cobwebs & hanging spiderwebs
    for wx, wy, wn in ((3, 2, 'mn_web_l'), (9, 1, 'mn_web_l'), (21, 1, 'mn_web_r'),
                       (7, 3, 'mn_webhang'), (15, 2, 'mn_webhang'), (19, 2, 'mn_webhang')):
        late.append((2, wx, wy, P1(wn)))

    # ---- 3. Act II Packing-Case Theatre Stage (x=14..20, y=4..7) ----
    # Crimson-gold woven stage carpet (14..19, 4..6) + glowing tin footlights along front apron (14..19, 7)!
    m.rug('R', 14, 4, 19, 6, medallion=False)
    for fx in range(14, 20):
        late.append((2, fx, 7, P1('mn_footlight')))
    # Painted castle backdrop flat behind Dame Rosamund (17..18, 3) & antique dressmaker's dummy at (15, 3) —
    # keeping Rag doll @ (13, 4), Attic stage sign @ (16, 4), Dame Rosamund @ (17, 5), & REVIVE @ (19, 5) 100% UNCLIPPED!
    m.on('mn_flats', 17, 3)
    m.on('mn_dummy', 15, 3)
    # Twin golden stage candelabras flanking the proscenium wings (13, 6) & (20, 6)!
    m.on('mn_candelabra', 13, 6)
    m.on('mn_candelabra', 20, 6)
    # East backstage prop trunks & hatboxes neatly stacked in the east wing (20..21, 4..5 & 21, 7..8)
    m.on('mn_trunk_open', 20, 4)
    m.on('mn_hatboxes', 21, 5)
    m.on('mn_trunk', 21, 8)
    m.on('mn_sheet_tall', 20, 9)

    # ---- 4. West Wardrobe & Dust-Sheeted Heirloom Alcove (x=2..8, y=4..10) ----
    # Theatrical costume rail, cracked standing mirror, and bookcase tucked cleanly against West Wing north wall (y=4..5)!
    m.on('mn_rail', 2, 4)       # (2..3, 4..5) costumes against west wall
    m.on('mn_mirror', 6, 4)     # (6, 4..5) cracked full-length dressing mirror
    m.on('mn_books', 8, 4)      # (8, 4..5) dusty playscript bookcase (FAR away from Rag doll @ 13,4!)
    # Draped grand heirloom cluster against west eaves: sheeted piano (2..4, 7..8) + gramophone + rocking horse + trunks!
    m.on('mn_sheet_piano', 2, 7)
    m.on('mn_rocking', 2, 10)
    m.on('mn_umbrella', 2, 11)
    m.on('mn_trunk', 5, 6)
    m.on('mn_globe', 6, 7)
    m.on('mn_candelabra', 7, 6)  # warm candle illuminating the west landing & heirloom alcove!
    m.on('mn_candelabra', 3, 12) # warm welcome candle right beside Stairs down (4,14) & arrival (4,11)!

    # ---- 5. Phantom Dust-Sheeted Audience Vignette Facing the Stage (x=9..19, y=9..12) ----
    # Clustered naturally in rows watching Act II — with Greavard @ (10, 11) nestled organically at the left front row!
    m.on('mn_sheet_table', 8, 9)     # (8..9, 9..10) draped stage-box heirloom table
    m.on('mn_sheet_sofa', 13, 9)     # (13..14, 9) draped phantom theatre settee facing stage!
    m.on('mn_sheet_chair', 12, 10)   # phantom audience chair
    m.on('mn_sheet_chair', 15, 10)   # phantom audience chair
    m.on('mn_sheet_chair', 17, 10)   # phantom audience chair
    m.on('mn_sheet_tall', 18, 9)     # tall shrouded statue watching from stage-right wings
    m.on('hb_crates4', 15, 12)       # (15..18, 12) stacked theatre packing cases along south eaves!
    m.on('mn_trunk', 19, 12)         # brass-bound costume trunk
    m.on('mn_hatboxes', 19, 11)
    m.on('mn_trunk_open', 11, 12)
    m.on('mn_gramophone', 13, 12)    # dusty antique gramophone playing Act II's silent overture!
    m.on('mn_flats', 9, 3)           # (9..10, 3..4) extra painted flat leaning cleanly against north wall west of oculus!

    # Cozy faded blue-navy runner guiding the player's eye from Hatch Arrival (4,11..13) across the Nave toward Stage!
    m.rug('B', 4, 11, 6, 13, medallion=False)
    m.rug('G', 10, 6, 12, 8, medallion=False)

    # Overhead gothic chandelier hovering softly over the Stage / Central Nave (pri=2, pas=0)!
    m.on('mn_chandelier', 15, 5)

    # ---- 6. Atmospheric Moonlight Shafts (cv_shaft), Floor Moonbeams & Warm Candelabra Glow Pools (pf_glow)! ----
    # Cool silver-blue moonlight pouring diagonally from Oculus (11,1) & West Window (5,2)
    for mx, my in ((11, 4), (12, 4), (12, 5), (13, 5), (5, 5), (6, 5)):
        late.append((2, mx, my, P1('mn_moon%d' % ((mx + my) % 2))))
    m.stamps.append(('cv_shaft', 11, 3))    # dramatic central oculus moonlight beam!
    m.stamps.append(('cv_shaft', 5, 4))     # west dormer window moonlight beam!
    # Warm golden candlelight glow pools contrasting with cold moonlight!
    for gx, gy in ((15, 5), (17, 5), (13, 6), (19, 6), (7, 6), (4, 12)):
        m.stamps.append(('pf_glow', gx, gy))

    # Subtle dust motes, wax drips & dusty footsteps from ladder toward the stage (never over solid furniture)
    for fx, fy in ((5, 11), (6, 10), (7, 9), (11, 8)):
        late.append((2, fx, fy, P1('mn_feet')))
    late.append((2, 14, 7, P1('mn_wax')))
    late.append((2, 4, 10, P1('mn_dust0')))
    late.append((2, 11, 6, P1('mn_dust1')))
    late.append((2, 16, 8, P1('mn_dust2')))
    late.append((2, 12, 11, P1('mn_dust0')))

    # ---- 7. Exact HEAD Events (6/6 preserved verbatim!) ----
    E += [
        {'type': 'warp', 'name': 'Stairs down', 'at': [4, 14], 'to': {'map': 546, 'x': 49, 'y': 24, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'event', 'name': 'Greavard', 'at': [10, 11], 'pages': [
            {'graphic': {'tile': P1('mn_sheet_chair')}, 'commands': [
                "Something under a dust sheet wags its tail.", {'script': 'WildBattle.start(:GREAVARD, 16)'}, {'selfswitch': ['A', True]}]},
            {'cond': {'self': 'A'}}]},
        {'type': 'item', 'at': [19, 5], 'item': 'REVIVE'},
        finale(),
        trial('Rag doll', (13, 4), 'ATTIC_DOLL', sprite='Followers/SHUPPET', condition='badges >= 14'),
        {'type': 'sign', 'name': 'Attic stage', 'at': [16, 4], 'post': False, 'text':
         "A little stage of packing-case boards, with tin footlights. Chalked on the back wall: ACT II - TONIGHT - AND EVERY NIGHT."},
    ]

    m.paint()

    # ---- 8. Post-Paint Multi-Wood Floor Craft (Unifies 547 with 546's rich walnut/mahogany/attic-pine hierarchy!) ----
    for y in range(4, H - 1):
        for x in range(2, W - 2):
            if m.cls[y, x] != '.' or m.cliff[y, x]:
                continue
            # Deep mahogany stage deck under Act II Stage (13..20, 4..7)
            if 13 <= x <= 20 and 4 <= y <= 7:
                m.L[0, y, x] = P1('N_f%d' % ((x + y) % 4))
            # Rich dark walnut parquet framing the central Oculus Nave & West Entry corridor (4..12, 5..13)
            elif (10 <= x <= 12 and 4 <= y <= 8) or (4 <= x <= 7 and 10 <= y <= 14):
                m.L[0, y, x] = P1('H_f%d' % ((x * 3 + y) % 4))
            # Keep raw aged attic pine planks (A_f0..3) in the outer storage eaves!

    PG.guard(m.L, 59)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '547.npy'), m.L.astype(np.int16))

    # Preserve exact 547 spec metadata & events verbatim (update only comment/raw cleanly)
    spec_path = os.path.join(SPEC_DIR, '547_thistledown_manor.yaml')
    old_spec = yaml.safe_load(open(spec_path))
    new_spec = {
        'id': 547,
        'name': old_spec['name'],
        'parent': old_spec['parent'],
        'bgm': old_spec['bgm'],
        'field': old_spec['field'],
        'metadata': old_spec['metadata'],
        'tone': [-22, -26, -2, 28],
        'raw': 'data/raw/547.npy',
        'tileset': 59,
        'events': old_spec['events'],
    }
    header = "# GENERATED by mapgen/layouts/wave8_story_craft.py (Wave 8 Map Craft): Thistledown Manor - Attic (547).\n"
    open(spec_path, 'w').write(header + yaml.safe_dump(new_spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f"Wrote data/raw/547.npy {m.L.shape} and updated {spec_path}")
    return m.L


# ================================================================================================
# MAP 3: 608 The Lowlight (Shattered - Post-Ch5) (60x44, Tileset 60 PF Rejuv Lumen)
# ================================================================================================
def build_608():
    W, H = 60, 44
    m = LumenCity(W, H, 608, base='l')
    m.ht[:] = 1
    m.roof_kind = 'T'

    # ---- 1. Exact 1-to-1 Architectural Unification with Wave 4's 181 Lumen Lowlight! ----
    # Spire north bulkhead, south/east abyssal drop to Nadir, NW Concourse landing
    m.cls[0:3, :] = 'x'; m.ht[0:3, :] = 2
    m.cls[0:3, 0:8] = 'p'; m.ht[0:3, 0:8] = 1
    m.cls[41:, :] = 'x'; m.ht[41:, :] = 0
    m.cls[:, 57:] = 'x'; m.ht[:, 57:] = 0
    m.rect(0, 3, 8, 8, 'p')

    reserve = {(47, y) for y in range(5, 11)} | {(48, y) for y in range(5, 11)} | {(49, y) for y in range(5, 11)}
    for x, y in reserve:
        m.taken[y, x] = True

    # Identical wet basalt street hierarchy as 181 (Shadow Row, Market Row, Edge Walk, Lift Lane, Pidove Steps)!
    m.rect(8, 12, 48, 1, 'r')
    m.rect(1, 25, 55, 1, 'r')
    m.rect(1, 38, 55, 1, 'r')
    m.rect(7, 11, 1, 28, 'r')
    m.rect(45, 11, 1, 28, 'r')
    # Rook's Undercity Market Court (22..35, 14..23): unified dark basalt outer ring + centered ashlar court (24..32, 15..22)!
    m.rect(22, 14, 14, 10, 'r')
    m.rect(24, 15, 9, 8, 'p')

    for x, y in ((9, 29), (10, 29), (9, 30), (10, 30), (9, 31), (10, 31)):
        m.taken[y, x] = True

    # Identical deterministic tenement block layout (use seed=181 RNG for exact building placement parity with 181!)
    m.seed = 181
    placed = []
    placed += lm_pack(m, 8, 46, 10, 5, PACK_LOW, seed=1)
    placed += lm_pack(m, 50, 56, 10, 5, PACK_LOW, seed=2)
    placed += lm_pack(m, 9, 21, 23, 14, PACK_LOW, seed=3)
    placed += lm_pack(m, 36, 43, 23, 14, PACK_LOW, seed=4)
    placed += lm_pack(m, 47, 56, 23, 14, PACK_LOW, seed=5)
    placed += lm_pack(m, 11, 25, 36, 27, PACK_LOW, seed=6)
    placed += lm_pack(m, 28, 43, 36, 27, PACK_LOW, seed=7)
    placed += lm_pack(m, 47, 56, 36, 27, PACK_LOW, seed=8)
    placed += lm_pack(m, 0, 5, 23, 14, PACK_LOW, seed=9)
    placed += lm_pack(m, 0, 5, 36, 27, PACK_LOW, seed=10)
    m.seed = 608

    # Identical alternating slate-blue & weathered tin roof districts as 181!
    slate_cells = set()
    for (x0, y0, x1, y1) in ((8, 5, 26, 10), (36, 14, 43, 23), (11, 27, 25, 36), (47, 27, 56, 36)):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] == 'f':
                    slate_cells.add((xx, yy))
    m.slate = slate_cells

    for x, y in reserve:
        m.taken[y, x] = False
    for x, y in ((9, 29), (10, 29), (9, 30), (10, 30), (9, 31), (10, 31)):
        m.taken[y, x] = False
    m.put('lm_lift', 9, 29, force=True)
    m.over.append((1, 8, 31, P1('lm_grate')))
    lm_door_events(m, placed, plaques=False)

    # ---- 2. Reserve ALL 27 Exact HEAD Events FIRST (ZERO prop collision with any Glassed Resident or Veil NPC!) ----
    E = m.events
    for nm, at in RES_AT.items():
        g = next((gp for n, s_, d, l, gp in ST.RES if n == nm), 2)
        m.stamp('lm_fixed%d' % g, at[0], at[1] - 1)
        m.keep_clear.add((at[0], at[1]))
        m.keep_clear.add((at[0], at[1] - 1))
        m.keep_clear.add((at[0], at[1] + 1))
        m.keep_clear.add((at[0] - 1, at[1]))
        m.keep_clear.add((at[0] + 1, at[1]))
    # Protect exact 27 HEAD event coords & 4-neighbors
    spec_path = os.path.join(SPEC_DIR, '608_lumen_lowlight_shattered.yaml')
    old_spec = yaml.safe_load(open(spec_path))
    for ev in old_spec['events']:
        ex, ey = ev['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            m.keep_clear.add((ex + dx, ey + dy))
    # Also protect main arterial walking lanes so NO barricade or crystal can EVER cause a softlock!
    main_corridors = (
        {(x, 12) for x in range(1, 56)}
        | {(x, 25) for x in range(1, 56)}
        | {(x, 38) for x in range(1, 56)}
        | {(7, y) for y in range(4, 39)}
        | {(45, y) for y in range(11, 39)}
        | {(48, y) for y in range(4, 13)}
        | {(x, y) for x in (26, 27, 28, 29, 30) for y in (15, 22)}
        | {(x, y) for x in range(0, 8) for y in range(4, 11)}
        | {(26, y) for y in range(25, 39)}
        | {(6, y) for y in range(11, 39)}
    )
    m.keep_clear |= main_corridors

    # ---- 3. Iconic Resident Storytelling Props (Frozen in the Shatter!) ----
    m.try_put('lm_noodles', 22, 14, on='qrp')     # Benno's noodle cart ("The steam is glass")
    m.try_put('lm_cobbler', 13, 24, on='lr')      # Old Jory's cobbler bench
    m.try_put('lm_ladder', 37, 12, on='lr')       # Hob Carrow's lamplighter ladder
    m.over.append((2, 40, 24, P1('lm_wear5')))    # Nessa's chalk hopscotch ("She's on six. Not seven.")
    for x, y in ((12, 11), (28, 11), (17, 24), (32, 24), (49, 24), (16, 37), (34, 37)):
        if m.free(x, y, 3, 1, on='lqrp'):
            m.stamp('lm_washline', x, y)

    # ---- 4. VISCERAL POST-SHATTER AFTERMATH: Wrecked Bazaar, Downed Pylons, Barricades, Crystalline Rift! ----
    # Dead unlit arc lamps across the entire district (unified coordinates with 181, ALL switched OFF!)
    dead_lamps = [
        (1, 3), (6, 3), (25, 15), (31, 15), (26, 23), (32, 23),
        (12, 26), (44, 26), (8, 33), (25, 39), (42, 39), (47, 10),
        (16, 13), (41, 13), (55, 12), (52, 26), (54, 39), (3, 12), (3, 39),
    ]
    lm_lamps(m, dead_lamps, name='lm_arclamp_off')

    # Shattered Market Court remnants: wrecked broadcast camera, snapped cables, knocked-over stalls/debris, fallen column!
    m.try_put('lm_cam', 30, 19, on='pqr')
    m.over.append((2, 27, 19, P1('lm_cables')))
    m.over.append((2, 28, 19, P1('lm_cables')))
    m.over.append((2, 29, 18, P1('lm_cables')))
    m.try_put('lm_junk0', 28, 21, on='pqr')
    m.try_put('lm_junk3', 32, 15, on='pqr')
    m.try_put('lm_junk1', 23, 21, on='pqr')
    m.try_put('lm_junk2', 33, 21, on='pqr')
    m.try_put('nr_colfall', 23, 22, on='pqr')     # fallen masonry girder across SW market apron!
    m.try_put('lm_pylon_off', 33, 15, on='pqr')   # darkened dead Lattice pylon standing fractured in NE plaza!
    for rx, ry in ((24, 18), (33, 18)):
        m.try_put('lm_ring', rx, ry, on='pqr')
    # Abandoned/shattered street stalls & debris clusters along back alleys
    for nm, sx, sy in (
        ('lm_junk0', 49, 37), ('lm_junk3', 54, 27), ('lm_junk3', 53, 13), ('lm_junk3', 5, 25),
        ('lm_junk1', 14, 38), ('lm_junk2', 45, 38), ('lm_junk1', 30, 12), ('lm_junk2', 19, 13),
        ('lm_junk0', 37, 26), ('lm_junk1', 41, 26), ('lm_junk2', 18, 39), ('lm_junk3', 50, 26),
        ('lm_bench', 9, 24), ('lm_bench', 27, 39), ('lm_viewer', 33, 39), ('lm_news', 38, 13),
        ('lm_steam0', 20, 25), ('lm_steam1', 46, 9), ('lm_steam0', 10, 32), ('lm_steam1', 35, 25),
        ('lm_vent', 26, 38), ('lm_vent', 44, 13), ('lm_vent', 15, 26),
    ):
        m.try_put(nm, sx, sy, on='lrpq')

    # Directorate Quarantine Barricades (`pf_barricade`) pinching back-alley sightlines & framing the NW Veil!
    for bx, by in (
        (1, 2), (4, 2),             # NW Veil overlook north quarantine barricades
        (2, 10), (5, 10),           # NW Veil south perimeter tape/barricades (keeps x=7 Lift Lane wide open!)
        (19, 11), (32, 11),         # Shadow Row back-alley sightline pinch points
        (24, 23), (32, 23),         # Shattered Market Court south quarantine tape
        (46, 13), (52, 24),         # East Shatter blast zone barricades (keeps Pidove Steps x=45 & Service Alley x=48 clear!)
        (15, 39), (38, 39),         # Edge Walk overlook cordons
    ):
        m.try_put('pf_barricade', bx, by, on='lrpq')

    # Flickering Amber Emergency Beacons (`lm_junction_on`, `cv_lamp_on`, `pf_beacon` / `lm_lamp_on`) cutting through the dark!
    for nm, ax, ay in (
        ('lm_junction_on', 6, 4),       # Directorate Veil checkpoint emergency beacon
        ('lm_junction_on', 1, 10),      # SW Veil checkpoint amber beacon
        ('lm_junction_on', 47, 5),      # Spire Service Door blast-zone warning beacon
        ('lm_junction_on', 25, 14),     # Market Court north amber emergency flare
        ('lm_junction_on', 34, 22),     # Market Court south amber emergency flare
        ('lm_junction_on', 9, 26),      # Lift Lane emergency beacon
        ('lm_junction_on', 44, 26),     # Pidove Steps emergency beacon
        ('lm_junction_on', 25, 39),     # Edge Walk overlook emergency beacon
        ('cv_lamp_on', 3, 2),           # Emergency work-lamp illuminating Valen/Testimony at the Veil!
        ('cv_lamp_on', 49, 6),          # Emergency work-lamp at Spire Service Door!
        ('cv_lamp_on', 23, 19),         # Flickering amber beacon beside Market Court wreckage!
        ('cv_lamp_on', 34, 14),         # Flickering beacon on NE Market Court!
    ):
        m.try_put(nm, ax, ay, on='lrpq')

    # VIOLENT DIAGONAL SHATTER RIFT tearing from Spire Service Door (48,5) -> Pidove Steps -> ACROSS Golden Sunburst -> Market Row!
    rng = random.Random(6088)
    rift_pts = [
        (48, 5), (47, 7), (46, 9), (45, 11), (43, 12), (40, 12), (37, 13),
        (34, 15), (32, 16), (30, 17), (28, 18), (26, 19), (24, 21), (22, 23), (20, 24), (18, 25),
        (15, 26), (12, 27), (44, 15), (44, 18), (44, 21), (43, 24),
    ]
    for rx, ry in rift_pts:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                xx, yy = rx + dx, ry + dy
                if not (1 <= xx < 56 and 4 <= yy < 40):
                    continue
                if m.cls[yy, xx] not in 'lrpq' or m.taken[yy, xx]:
                    continue
                dist = abs(dx) + abs(dy)
                if dist == 0:
                    m.over.append((1, xx, yy, P1('gd_crack%d' % ((xx + yy) % 2))))
                    m.over.append((2, xx, yy, P1('lm_bleed%d' % ((xx * 3 + yy) % 3))))
                elif dist == 1 and rng.random() < 0.78:
                    m.over.append((2, xx, yy, P1('lm_bleed%d' % rng.randrange(3))))

    # Sculpted Asymmetric Crystalline Debris Clusters (tall spires + low crystal shards along rift & blast margins!)
    crystal_clusters = [
        # Blast epicenter around Spire Service Door (48,4)
        (49, 8, 'cr_purple_t'), (46, 10, 'cr_teal_e'), (49, 10, 'cr_purple_c'),
        # Shattered Sunburst Market Court crystal eruptions (framing the diagonal rift, NEVER blocking paths!)
        (35, 14, 'cr_purple_t'), (34, 15, 'cr_teal_c'), (35, 22, 'cr_teal_t'),
        (22, 22, 'cr_purple_t'), (23, 15, 'cr_teal_e'), (31, 16, 'cr_purple_e'),
        (26, 21, 'cr_purple_c'), (29, 15, 'cr_teal_c'), (25, 19, 'cr_blue_c'),
        # Secondary shockwave crystal eruptions down Pidove Steps, Shadow Row & Market Row
        (44, 14, 'cr_teal_t'), (46, 26, 'cr_purple_t'), (44, 24, 'cr_teal_c'),
        (19, 24, 'cr_purple_e'), (18, 26, 'cr_teal_c'), (10, 26, 'cr_purple_c'),
        (38, 12, 'cr_purple_c'), (26, 11, 'cr_teal_c'), (51, 12, 'cr_purple_e'),
        (31, 39, 'cr_purple_c'), (48, 39, 'cr_teal_e'), (11, 39, 'cr_purple_c'),
    ]
    for cx, cy, nm in crystal_clusters:
        st_c = CK.STAMPS[nm]
        cw, ch = len(st_c['layers'][0][0]), len(st_c['layers'][0])
        if all((cx + dx, cy + dy) not in m.keep_clear for dx in range(cw) for dy in range(ch)):
            if m.free(cx, cy, cw, ch, on='lrpq'):
                m.stamp(nm, cx, cy)

    # Shimmering Violet Bleed Glass Shards across the Shattered streets (denser near the Spire & Rift!)
    for y in range(3, 41):
        for x in range(1, 56):
            if m.cls[y, x] in 'lrpq' and not m.taken[y, x]:
                near_rift = abs((x - 28) * 0.55 + (y - 18)) < 11
                prob = 0.24 if near_rift else 0.13
                if rng.random() < prob:
                    m.over.append((2, x, y, P1('lm_bleed%d' % rng.randrange(3))))

    # Shimmering Violet Veil Curtain along West Border (x=0, y=3..10)
    for y in range(3, 11):
        m.over.append((2, 0, y, P1('lm_veil%d' % (y % 3))))

    # ---- 5. Abyssal Nadir Edge Landmarks (Darkened Dead Spire Pylons, Broken South Brass Railings & Rising Smoke!) ----
    def abyss_piece(name, x, y):
        st = CK.STAMPS[name]
        h, w = len(st['layers'][0]), len(st['layers'][0][0])
        for dy in range(h):
            for dx in range(w):
                for z in (1, 2):
                    t = st['layers'][z][dy][dx]
                    if t and m.inb(x + dx, y + dy):
                        m.over.append((z, x + dx, y + dy, t))

    for py in (6, 17, 29):
        abyss_piece('lm_pylon_off', 58, py)      # Dead darkened Nadir pylons (visceral contrast with 181's lit pylons!)
    for ry in (12, 24, 36):
        abyss_piece('lm_ring', 58, ry)
    for rx in (10, 23, 37, 50):
        abyss_piece('lm_ring', rx, 42)
    abyss_piece('lm_steam0', 57, 14)
    abyss_piece('lm_steam1', 57, 26)
    abyss_piece('lm_steam0', 29, 42)
    abyss_piece('lm_steam1', 48, 42)
    # NW Overlook brass railing
    for x in range(1, 7):
        m.over.append((1, x, 2, P1('lm_bollard' if x in (1, 6) else 'lm_railing_m')))
    # South Overlook forged brass railings — WITH DRAMATIC SHATTER-BLOWN GAPS at x=22..25 & x=42..45!
    for x in range(2, 56, 4):
        if x in (22, 33, 42):
            m.over.append((1, x, 40, P1('lm_bollard')))  # snapped lonely bollard where the railing gave way!
            continue
        m.over.append((1, x, 40, P1('lm_bollard')))
        if x + 1 < 56:
            m.over.append((1, x + 1, 40, P1('lm_railing_w')))
        if x + 2 < 56:
            m.over.append((1, x + 2, 40, P1('lm_railing_m')))
        if x + 3 < 56:
            m.over.append((1, x + 3, 40, P1('lm_railing_e')))

    # ---- 6. Eerie Broken-Prism Shafts & Amber Emergency Beacon Glow Pools! ----
    for sx, sy in ((47, 4), (27, 17), (2, 5)):
        m.stamps.append(('cv_shaft', sx, sy))    # Eerie shattered-vault & veil light shafts!
    for gx, gy in (
        (47, 4), (48, 6),          # Glowing violet-amber breach pouring out of Spire Service Door!
        (2, 6), (5, 5), (5, 8),    # Amber emergency beacons at the NW Veil quarantine checkpoint!
        (28, 18), (24, 15), (33, 21),  # Shattered Sunburst Court crystalline rift & beacon glows!
        (9, 26), (44, 26), (25, 39),   # Emergency intersection flares cutting the blackout!
    ):
        m.stamps.append(('pf_glow', gx, gy))

    lm_scatter_wear(m, 8, on='lqr', seed=608, kinds=(0, 1, 2, 3))
    m.paint()

    # ---- 7. Post-Paint Architectural Unification with 181 (Obsidian Market Court, Cracked Sunburst, Torn Carpet!) ----
    walkable_base = {0, P1('lm_road0'), P1('lm_road1'), P1('lm_low0'), P1('lm_low1'), P1('lm_low2'), P1('lm_low3'),
                     P1('lm_plaza0'), P1('lm_plaza1'),
                     P1('lm_pave0'), P1('lm_pave1'), P1('lm_pave2'), P1('lm_pave3'), P1('lm_pave4'), P1('lm_pave5'), P1('lm_pave6'), P1('lm_pave7')}
    # Symmetric Octagonal Obsidian & Wet Basalt Market Court framing the centered 5x5 Golden Sunburst (x=26..30, y=16..20)!
    for y in range(14, 24):
        for x in range(22, 36):
            in_inner = (25 <= x <= 31 and 15 <= y <= 21) and (x, y) not in {(25, 15), (31, 15), (25, 21), (31, 21)}
            in_curb = (24 <= x <= 32 and 14 <= y <= 22) and not in_inner
            is_ground = (m.L[1, y, x] in walkable_base) or (not m.taken[y, x] and m.L[1, y, x] == m.L[0, y, x])
            if not in_inner and is_ground:
                t = P1('Z_f0') if in_curb else P1('lm_road%d' % ((x + y) & 1))
                m.L[0, y, x] = t
                m.L[1, y, x] = t
    # 5x5 Golden Meridian Sunburst Medallion underneath the Market Court — CRACKED diagonally by the Shatter Rift!
    sun_L = CK.STAMPS['lm_sun']['layers'][0]
    rift_cut = {(30, 16), (29, 17), (28, 18), (27, 19), (26, 20)}
    for dy in range(5):
        for dx in range(5):
            xx, yy = 26 + dx, 16 + dy
            t = sun_L[dy][dx]
            if t:
                m.L[0, yy, xx] = t
                if (xx, yy) in rift_cut:
                    m.L[1, yy, xx] = P1('gd_crack%d' % ((xx + yy) % 2))
                    m.L[2, yy, xx] = P1('lm_bleed%d' % ((xx * 3 + yy) % 3))
                elif m.L[1, yy, xx] in walkable_base:
                    m.L[1, yy, xx] = t

    # NW Upper-Spire Overlook: dark obsidian frame + crimson carpet (matching 181, now scarred with glass!)
    for y in range(0, 11):
        for x in range(0, 8):
            if (x in (0, 7) or y in (0, 1, 10)) and m.L[1, y, x] in walkable_base:
                m.L[0, y, x] = P1('Z_f0')
                m.L[1, y, x] = P1('Z_f0')
    for y in range(4, 9):
        for x in (2, 3, 4):
            if m.L[1, y, x] in walkable_base:
                part = ('n' if y == 4 else 's' if y == 8 else '') + ('w' if x == 2 else 'e' if x == 4 else '')
                t = P1('lm_carpet_' + (part or 'c'))
                m.L[0, y, x] = t
                m.L[1, y, x] = t

    # Clandestine Spire Service Door Alley (47..49, 5..10): obsidian deck + dead/cracked grates!
    for y in range(5, 11):
        for x in (47, 48, 49):
            t = P1('lm_grate_off') if x == 48 else P1('Z_f0')
            m.L[0, y, x] = t
            if m.L[1, y, x] in walkable_base:
                m.L[1, y, x] = t

    # Industrial street grates (unlit/shattered) along avenues & Lift Plaza
    for gx, gy in [(7, 12), (7, 25), (7, 30), (8, 30), (7, 32), (8, 32),
                   (18, 25), (28, 25), (38, 25), (45, 12), (45, 25), (45, 38),
                   (20, 12), (35, 12), (48, 12), (28, 38), (3, 10), (4, 10), (5, 10)]:
        if m.L[1, gy, gx] in walkable_base:
            m.L[0, gy, gx] = P1('lm_grate_off')
            m.L[1, gy, gx] = P1('lm_grate_off')

    # Rooftop vents/skylights on tenement blocks (matching 181!)
    rng_r = random.Random(1819)
    for yy in range(5, 36):
        for xx in range(1, 56):
            if m.cls[yy, xx] == 'f' and m.L[1, yy, xx] == 0 and rng_r.random() < 0.045:
                m.L[1, yy, xx] = P1('lm_grate_off')

    # NW overlook kerbs
    kS, kE = P1('lm_kerbS'), P1('lm_kerbE')
    for x in range(1, 8):
        if m.L[1, 10, x] == 0:
            m.L[1, 10, x] = kS
    for y in range(3, 10):
        if m.L[1, y, 7] == 0 and (7, y) not in m.keep_clear:
            m.L[1, y, 7] = kE

    # Spire Service Door stamp on north bulkhead (48, 3..4)
    sd = CK.STAMPS['lm_sdoor']['layers']
    m.L[2, 3, 48] = next(sd[z][0][0] for z in range(3) if sd[z][0][0])
    m.L[2, 4, 48] = next(sd[z][1][0] for z in range(3) if sd[z][1][0])

    # Seal west edge cleanly outside The Veil warps (y=4..10)
    m.seal_edges([('W', 4, 7)], filler=P1('lm_bollard'), sides='W')
    PG.guard(m.L, 60)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '608.npy'), m.L.astype(np.int16))

    # Preserve exact 27 HEAD events & metadata cleanly!
    new_spec = {
        'id': 608,
        'name': old_spec['name'],
        'parent': old_spec['parent'],
        'bgm': old_spec['bgm'],
        'rubric': True,
        'field': old_spec['field'],
        'metadata': old_spec['metadata'],
        'tone': [-36, -44, 14, 52],
        'fog': old_spec['fog'],
        'raw': 'data/raw/608.npy',
        'tileset': 60,
        'events': old_spec['events'],
    }
    header = "# GENERATED by mapgen/layouts/wave8_story_craft.py (Wave 8 Map Craft): The Lowlight (Shattered) (608).\n"
    open(spec_path, 'w').write(header + yaml.safe_dump(new_spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f"Wrote data/raw/608.npy {m.L.shape} and updated {spec_path}")
    return m.L


# ================================================================================================
# MAP 4: 183 Lumen Arcade 1F (21x12, Tileset 34 Prismfall Interior)
# TOUCHES ONLY MAP 183 INSIDE 182_lumen_pc_arcade.yaml; LEAVES MAP 182 100% UNTOUCHED!
# ================================================================================================
def _compress_tile_edits(L):
    """Encode (3, H, W) array cleanly as compact build.py tile_edits (rect-fills) so
    template: mart keeps 100% HEAD event IDs (#2 Mart @ 2,3; #3 Exit @ 4,8) & scripts verbatim!"""
    _, H, W = L.shape
    edits = [[0, 0, 0, W, H, 0], [1, 0, 0, W, H, 0], [2, 0, 0, W, H, 0]]
    for z in range(3):
        for y in range(H):
            x = 0
            while x < W:
                t = int(L[z, y, x])
                if t == 0:
                    x += 1
                    continue
                x1 = x + 1
                while x1 < W and int(L[z, y, x1]) == t:
                    x1 += 1
                w = x1 - x
                if w == 1:
                    edits.append([z, x, y, t])
                else:
                    edits.append([z, x, y, w, 1, t])
                x = x1
    return edits


def build_183():
    # Exact stretched dimensions from mart.json (11x9) via stretch: [['x', 10, 10], ['y', 8, 3]] -> 21x12!
    # Preserves EXACT HEAD events:
    #   #2 'Mart' @ (2, 3) (dir=6 right, exact badge-scaled pbPokemonMart script!)
    #   #3 'Exit' @ (4, 8) -> Map 180 (40, 45) (incoming arrival from 180 LC_DEPT lands @ (4, 7) up!)
    TID = 34
    VOID = 5437
    W, H = 21, 12
    L = np.zeros((3, H, W), dtype=np.int32)
    L[0, :, :] = VOID

    # ---- 1. Void-Sculpted Cyberpunk-DS Arcade Silhouette (Stepped L-Hall + Chamfered Lounges!) ----
    # West Prize Counter & Entry Vestibule: x=1..6, y=2..7 + recessed Entry Door Notch x=3..5, y=8!
    # Central Glowing Neon Game Floor:      x=7..15, y=2..10 (steps 2 rows deeper south into High-Roller Holo Lounge!)
    # East Recessed Cyber-Vending Alcove:   x=16..19, y=3..8 (stepped 1 row inward north & chamfered SE into black void!)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:7] = True          # West prize counter & vestibule (x=1..6, y=2..7)
    floor[8, 3:6] = True            # Recessed south entry notch (x=3..5, y=8; Exit @ 4,8!)
    floor[7, 1] = False             # SW corner chamfer into void
    floor[2:11, 7:16] = True        # Central arcade floor & south holo lounge (x=7..15, y=2..10)
    floor[10, 7] = False            # South lounge SW chamfer
    floor[10, 15] = False           # South lounge SE chamfer
    floor[3:9, 16:20] = True        # East cyber-vending & gaming PC alcove (x=16..19, y=3..8)
    floor[8, 19] = False            # SE alcove chamfer

    # 2-row sleek dark-steel / neon-blue arcade north walls above every floor boundary!
    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(2, H):
        for x in range(1, W - 1):
            if floor[y, x] and not floor[y - 1, x]:
                wall_face[y - 1, x] = True
                if y - 2 >= 0:
                    wall_face[y - 2, x] = True

    interior = floor | wall_face

    # ---- 2. Auto-Seamed Sleek Cyberpunk-Blue Wall Trim & Dark Diamond Luxury Floors ----
    # Dark sleek obsidian-diamond floor (7737/7745 dark diamond carpet, pas=0) & dark slate (7091/7092/7099/7100)
    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                L[0, y, x] = 7737 if (x + y) % 2 == 0 else 7745
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                # Sleek modern dark-steel & electric-blue illuminated arcade paneling!
                # Row 0 (upper): 7520/7521/7522 crisp silver-framed top header + neon blue glass
                # Row 1 (lower): 7536/7537/7538 dark steel kickplate + blue glow trim
                left_end = not wall_face[y, x - 1]
                right_end = not wall_face[y, x + 1]
                if left_end:
                    L[0, y, x] = 7536 if is_lower else 7520
                elif right_end:
                    L[0, y, x] = 7538 if is_lower else 7522
                else:
                    L[0, y, x] = 7537 if is_lower else 7521
            else:
                # Sleek Electric-Blue Perimeter Trim (7552..7570) framing the sculpted void silhouette!
                N = y > 0 and interior[y - 1, x]
                S = y + 1 < H and interior[y + 1, x]
                W_ = x > 0 and interior[y, x - 1]
                E = x + 1 < W and interior[y, x + 1]
                NW = y > 0 and x > 0 and interior[y - 1, x - 1]
                NE = y > 0 and x + 1 < W and interior[y - 1, x + 1]
                SW = y + 1 < H and x > 0 and interior[y + 1, x - 1]
                SE = y + 1 < H and x + 1 < W and interior[y + 1, x + 1]
                if S and E:
                    L[0, y, x] = 7564
                elif S and W_:
                    L[0, y, x] = 7563
                elif N and E:
                    L[0, y, x] = 7556
                elif N and W_:
                    L[0, y, x] = 7555
                elif S:
                    L[0, y, x] = 7569
                elif N:
                    L[0, y, x] = 7553
                elif E:
                    L[0, y, x] = 7562
                elif W_:
                    L[0, y, x] = 7560
                elif SE:
                    L[0, y, x] = 7570
                elif SW:
                    L[0, y, x] = 7568
                elif NE:
                    L[0, y, x] = 7554
                elif NW:
                    L[0, y, x] = 7552

    # ---- 3. Neon Carpet Lanes, Glowing Cyan Floor Pads & Multi-Zone Arcade Flooring ----
    BLUE_CARPET = [[7496, 7497, 7498], [7504, 7505, 7506], [7512, 7513, 7514]]
    RED_CARPET = [[7172, 7173, 7174], [7180, 7181, 7182], [7188, 7189, 7190]]
    DARK_SLATE = [[7091, 7092, 7091], [7099, 7100, 7099], [7091, 7092, 7091]]

    # West Prize Booth behind-counter slate pad (x=1..2, y=2..4)
    for y in range(2, 5):
        for x in (1, 2):
            L[0, y, x] = 7091 if (x + y) % 2 == 0 else 7092

    # Glowing Crimson Arrival Carpet Lane from Exit (4,8) straight north through the Entry Vestibule (x=3..5, y=4..8)!
    _put_9slice(L, RED_CARPET, 3, 5, 5, 7, z=1)
    # Classic Arcade welcome mat right on Exit (4, 8)
    L[1, 8, 4] = 444
    L[0, 8, 3] = 7099; L[0, 8, 4] = 7100; L[0, 8, 5] = 7099

    # Royal Electric-Blue Neon Carpet Spine guiding players through the Main Cabinet Floor (x=6..15, y=6..7)
    _put_9slice(L, BLUE_CARPET, 6, 6, 15, 7, z=1)
    # High-Roller Holo Lounge Crimson Medallion Carpet (x=9..13, y=8..10)
    _put_9slice(L, RED_CARPET, 9, 8, 13, 10, z=1)
    # East Cyber-Alley dark slate floor
    for y in range(3, 9):
        for x in range(16, 20):
            if floor[y, x]:
                L[0, y, x] = 7099 if (x + y) % 2 == 0 else 7100

    # Ambient Glowing Cyan Neon Floor Accent Pads (725 = glowing electric-cyan floor tile, pas=0!)
    # Creating authentic cyberpunk-DS neon floor glow pools around the cabinet islands, prize booth & holo pod!
    for gx, gy in ((4, 3), (4, 4), (6, 2), (6, 3), (6, 4), (6, 5),
                   (7, 2), (10, 2), (11, 2), (14, 2), (15, 2),
                   (7, 5), (11, 5), (15, 5),
                   (8, 8), (14, 8), (8, 9), (14, 9),
                   (16, 4), (16, 5), (16, 6), (17, 7), (18, 7)):
        if floor[gy, gx]:
            L[0, gy, gx] = 725

    # ---- 4. Sleek Prize & Mart Counter Booth (100% HEAD #2 Mart @ 2,3 Compatible!) ----
    # Mart clerk (#2) stands at (2, 3) facing RIGHT!
    # Vertical counter with REAL 0x80 counter flag at (3, 3) & (3, 4) so Essentials shopping from (4, 3) works natively!
    # PLUS leave (1, 4) cleanly passable so strict 4-neighbor BFS from (4, 7) ALSO reaches (1, 3) adjacent to Mart (2, 3)!
    # Chrisola Blue Marble Counter tiles:
    #   (3, 2) = 7227 (top vertical arm, pas=15)
    #   (3, 3) = 7235 (vertical arm w/ flower & 0x80 COUNTER FLAG!)
    #   (3, 4) = 7243 (SE corner counter w/ 0x80 COUNTER FLAG!)
    #   (2, 4) = 7241 (front counter w/ cash register & 0x80 COUNTER FLAG!)
    L[1, 2, 3] = 7227
    L[1, 3, 3] = 7235
    L[1, 4, 3] = 7243
    L[1, 4, 2] = 7241
    # Prize plushies & display case tucked cleanly in the SW corner (x=1..2, y=6) (leaves y=5 & (1,4) wide open!)
    L[1, 6, 1] = 7128; L[1, 6, 2] = 7129  # Glass prize display case (0x80)
    L[2, 5, 1] = 7120; L[2, 5, 2] = 7121  # Glass case upper rim (pri=5)
    # Neon wall posters & glowing arcade screens along BOTH the main north wall (y=0..1) & East Alcove wall (y=1..2)!
    for wx in (2, 5, 11, 14):
        L[1, 0, wx] = 7718 if wx % 2 == 0 else 7719
        L[1, 1, wx] = 7726 if wx % 2 == 0 else 7727
    # Dress East Cyber-Alley north wall (17..19, 1..2) with matching glowing neon screens & retro tech panels!
    L[1, 1, 17] = 7719; L[1, 2, 17] = 7727
    L[1, 1, 18] = 7718; L[1, 2, 18] = 7726
    L[1, 2, 19] = 7732

    # ---- 5. Clustered Arcade Cabinet Islands, Prize Roulette, Holo-Pod & Gaming PCs! ----
    # Island A (North-Center, x=7..9, y=2..4): Back-to-back Rejuvenation Blue Arcade Cabinet Pair + Prize Scoreboard!
    # Dual Blue Arcade Machines (2x3: 7283..7284 / 7291..7292 / 7299..7300) at (8..9, 3..5) -> wait: put at (7..8, 3..5)!
    ARCADE_PAIR = [
        [7283, 7284],
        [7291, 7292],
        [7299, 7300],
    ]
    _put_grid(L, ARCADE_PAIR, 7, 3, z_rows=(2, 1, 1))
    # Side-facing blue cabinet (1x2: 7307/7315) at (9, 3..4) + prize stool / glowing pad!
    L[2, 3, 9] = 7307
    L[1, 4, 9] = 7315

    # Island B (Center-East, x=12..14, y=2..5): 3x3 Neon-Blue Prize Roulette / Game Island (7280..7298)!
    ROULETTE_ISLAND = [
        [7280, 7281, 7282],
        [7288, 7289, 7290],
        [7296, 7297, 7298],
    ]
    _put_grid(L, ROULETTE_ISLAND, 12, 3, z_rows=(1, 1, 1))
    # Green Arcade Scoreboard / Ticket Board mounted cleanly on the North Wall above the floor (x=7..9, y=0..1)!
    SCOREBOARD_WALL = [
        [7312, 7313, 7314],
        [7320, 7321, 7322],
    ]
    _put_grid(L, SCOREBOARD_WALL, 7, 0, z_rows=(1, 1))
    # Prize Display Shelf (2x3: 7277..7278 / 7285..7286 / 7293..7294) anchored cleanly at (4..5, 1..2) right beside Prize Counter!
    PRIZE_SHELF = [
        [7277, 7278],
        [7285, 7286],
        [7293, 7294],
    ]
    _put_grid(L, PRIZE_SHELF, 4, 0, z_rows=(2, 2, 1))

    # South High-Roller Hologram Lounge (x=9..13, y=8..10):
    # Glowing Violet Holo-Capsule Pod (2x3: 7154..7155 / 7162..7163 / 7170..7171) centered at (10..11, 7..9)!
    # Keep y=7 walkway open on x=6..9 & x=12..15, so put Holo-Pod centered at (10..11, 8..10) -> wait: height 3 at y=8..10!
    # Check passability of 7154..7171: all 6 tiles are pas=15, pri=0, so players walk cleanly around x=9 & x=12 & y=7!
    HOLO_POD = [
        [7154, 7155],
        [7162, 7163],
        [7170, 7171],
    ]
    _put_grid(L, HOLO_POD, 10, 8, z_rows=(2, 1, 1))
    # Plush Arcade Prize Showcase flanking the Holo Lounge (Eevee, Poké Balls, Magikarp on display pedestals!)
    # Sleek silver lounge sofa (7571..7573 / 7579..7581) on West/East lounge flanks? Place sleek prize displays at (8, 9) & (14, 9)!
    L[1, 9, 8] = 4416; L[2, 8, 8] = 4408    # Ticket/arcade prize machine on SW lounge wing
    L[1, 9, 14] = 4417; L[2, 8, 14] = 4409  # Companion prize machine on SE lounge wing

    # East Cyber-Alley & Gaming PC Alcove (x=16..19, y=3..8):
    # Multi-Screen Gaming PC Rig (7712..7714 / 7720..7722 / 7728..7730 -> top 2 rows solid, bottom row walkable shadow) at (17..19, 3..4)!
    GAMING_PC = [
        [7712, 7713, 7714],
        [7720, 7721, 7722],
    ]
    _put_grid(L, GAMING_PC, 17, 3, z_rows=(2, 1))
    # Second dual blue arcade cabinet pair in SE East Alcove (x=18..19, y=5..7)
    _put_grid(L, ARCADE_PAIR, 18, 5, z_rows=(2, 1, 1))
    # Glowing Blue Token/Drink Vending Machine (2342/2350) tucked into north cyber-corner (16, 2..3)!
    L[2, 2, 16] = 2342
    L[1, 3, 16] = 2350

    # Lush Parlor Palms framing the Arcade Entrance & Lounge Wings (7126 pri=5 top, 7134 pas=15 pot!)
    for px, py in ((6, 7), (15, 2), (16, 8)):
        L[2, py - 1, px] = 7126
        L[1, py, px] = 7134

    # Guarantee 100% passability on critical arrival/exit/mart-access cells!
    for cx, cy in ((4, 8), (4, 7), (4, 6), (4, 5), (4, 4), (4, 3), (1, 4), (1, 3), (2, 3), (2, 2), (1, 2)):
        if (cx, cy) == (4, 8):
            continue
        if L[1, cy, cx] in (7227, 7235, 7243, 7241):
            continue
        # Ensure nothing accidentally blocked the corridor

    PG.guard(L, TID)

    # Save exact raw array to mapgen/data/raw/183.npy!
    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '183.npy'), L.astype(np.int16))

    # Update ONLY Map 183 inside mapgen/specs/182_lumen_pc_arcade.yaml — LEAVE MAP 182 100% BYTE-IDENTICAL!
    spec_path = os.path.join(SPEC_DIR, '182_lumen_pc_arcade.yaml')
    raw_txt = open(spec_path, 'r', encoding='utf-8').read()
    parts = raw_txt.split('\n---\n')
    assert len(parts) == 2, f"Expected 2 docs in 182_lumen_pc_arcade.yaml, got {len(parts)}"
    doc182_verbatim = parts[0]
    old183 = yaml.safe_load(parts[1])
    assert old183.get('id') == 183

    new183 = {
        'id': 183,
        'name': old183['name'],
        'parent': old183['parent'],
        'template': 'mart',
        'exit_link': 'LC_DEPT',
        'drop_template_events': ['Questionnaire', 'Deliveryman'],
        'tileset': TID,
        'bgm': old183['bgm'],
        'tone': [-12, -8, 12, 8],
        'metadata': old183['metadata'],
        'stretch': [['x', 10, 10], ['y', 8, 3]],
        'tile_edits': _compress_tile_edits(L),
        'events': [],
    }
    doc183_txt = "# Map 183 revamped by layouts/wave8_story_craft.py (Wave 8 Map Craft; data/raw/183.npy).\n" + yaml.safe_dump(
        new183, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True
    )
    open(spec_path, 'w', encoding='utf-8').write(doc182_verbatim + '\n---\n' + doc183_txt)
    print(f"Wrote data/raw/183.npy {L.shape} and updated ONLY Map 183 in {spec_path} ({len(new183['tile_edits'])} edits)")
    return L


# ================================================================================================
# MAP 5: 187 Glide Cycles (19x12, Tileset 60 PF Rejuv Lumen)
# ================================================================================================
def build_187():
    # Iconic Lumen City Brass-and-Glass Bicycle Showroom (where players receive their Bicycle!).
    # Preserves 100% HEAD events & coords:
    #   #1 'Exit'       @ (6, 9) -> Map 180 (53, 45) (incoming arrival from 180 LC_BIKE lands @ (6, 8) up!)
    #   #2 'Shopkeeper' @ (4, 5) (NPC 12, facing down)
    W, H = 19, 12
    m = Cave(W, H, 'Y', 187, pool='Cave Pool', tid=60)
    m.STAIRS = LK.STAIRS_LM or LK.K.STAIRS_STONE
    m.kit = {TER: 'lmw', FLOOR: 'cvY', 'default': 'cvY'}

    # ---- 1. Void-Sculpted Three-Bay Boutique Showroom Silhouette (ZERO rectangular checker box!) ----
    # West Sales & Gala Reception Boutique: x=1..7, y=3..8 + recessed Entry Portal x=5..7, y=9 (Exit @ 6,9!)
    # Central Flagship Cycle Showroom Bay:  x=8..13, y=3..10 (steps 1 row deeper south for Bike-Rack Fitting Bay!)
    # East Mechanic Repair Bench Alcove:    x=14..17, y=3..9 (contrasting dark-slate workshop alcove, chamfered SE!)
    m.box(1, 3, 7, 8, FLOOR, '.')
    m.box(5, 9, 7, 9, FLOOR, '.')
    m.box(8, 3, 13, 10, FLOOR, '.')
    m.box(14, 3, 17, 9, FLOOR, '.')

    # Sculpted void chamfers along outer SW & SE showroom corners
    m.mass_at([
        (1, 8), (2, 8),           # SW chamfered reception corner
        (17, 9), (16, 9),         # SE chamfered workshop corner
        (8, 10), (13, 10),        # Beveled south fitting-bay shoulders
    ])

    # ---- 2. Sculpted Elevated Marble Flagship Cycle Display Podium (TER, lmw ashlar, x=9..12, y=3..6) ----
    # Rises majestically right beside the central showroom promenade — approached via sleek marble steps at (10..11, 6..8)!
    # Wait: with rows=3 cliffs on TER at y=3..6, lip=y=6, face=y=7, base=y=8 -> let's keep TER compact at y=3..5
    # so the walkable podium deck is y=5 (x=9..12) with crisp marble face at y=6 and 2-wide steps at (10..11, 5..7)?
    # Even cleaner: use a flush 5x5 Golden Sunburst Showcase Podium framed by brass railings & inlaid marble trim
    # in the Central Showroom (x=8..13, y=5..9) so players have wide, effortless 360-degree showroom circulation
    # AND zero cramped stair walls in a 12-tall boutique!
    m.plan_cliffs(rows=3)

    # Protect ALL critical walkways, arrival (6,8), Exit (6,9), & Shopkeeper (4,5) + direct talk cell (4,6)!
    m.keep_clear |= (
        {(6, y) for y in range(5, 10)}
        | {(5, 8), (7, 8), (5, 9), (7, 9)}
        | {(4, 5), (4, 6), (5, 5), (5, 6), (3, 6)}
        | {(x, 7) for x in range(4, 16)}
        | {(8, y) for y in range(5, 10)}
        | {(13, y) for y in range(5, 10)}
    )

    def put_if(name, x, y):
        st = CK.STAMPS[name]
        w, h = len(st['layers'][0][0]), len(st['layers'][0])
        if m.free(x, y, w, h, on='.') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
            m.put(name, x, y)
            return True
        return False

    def hang_wall(name, x, y):
        st = CK.STAMPS[name]['layers']
        for dy in range(len(st[0])):
            for dx in range(len(st[0][0])):
                t = next((st[z][dy][dx] for z in (2, 1, 0) if st[z][dy][dx]), 0)
                if t and m.inb(x + dx, y + dy) and m.cliff[y + dy, x + dx]:
                    m.over.append((2, x + dx, y + dy, t))

    # ---- 3. Grand North Showroom Bulkhead (Panoramic Windows, Gala Banners, CAD Monitors & Posters) ----
    for wx in (2, 7, 12):
        hang_wall('lm_window', wx, 2)
    hang_wall('lm_banner_w', 4, 2)       # Royal crimson Meridian Gala promo banner behind Shopkeeper!
    hang_wall('lm_banner_w', 9, 2)       # Gala promo banner framing Central Flagship Cycle Podium
    hang_wall('lm_banner', 11, 2)        # Meridian navy-gold banner
    hang_wall('lm_monitors', 15, 2)      # Bicycle frame CAD & spoke telemetry screens above Mechanic Repair Bench!
    for px, py, nm in ((3, 3, 'lm_poster0'), (6, 3, 'lm_poster2'), (10, 3, 'lm_poster1'), (14, 3, 'lm_alarm_on')):
        if m.cliff[py, px]:
            m.over.append((2, px, py, P1(nm)))

    # ---- 4. West Sales & Gala Reception Boutique (x=1..7, y=5..8) ----
    # Sleek cream-brass sales counter right beside Shopkeeper (4,5) -> leaves (4,6) & (5,5) wide open for direct talk!
    m.over.append((1, 2, 5, P1('lm_counter_l')))
    m.over.append((1, 3, 5, P1('lm_counter_m')))
    m.taken[5, 2] = True; m.taken[5, 3] = True
    put_if('lm_plant', 1, 5)             # Welcoming parlor greenery in NW corner
    put_if('lm_planter', 3, 8)           # Floral planter framing the SW entry chamfer
    put_if('lm_lamp_on', 2, 6)           # Warm brass reception lamp

    # ---- 5. Central Flagship Cycle Display Podium & Bike-Rack Showroom Bays (x=8..13, y=5..10) ----
    # Illuminated Glass Showcase Cases (`lm_case`) displaying custom brass frames & gears along the north showcase wall!
    put_if('lm_case', 9, 4)              # (9..10, 4..5) Flagship Brass-Frame Showcase Case!
    put_if('lm_case', 11, 4)             # (11..12, 4..5) Glass-Spoke Prototype Showcase Case!
    # Mounted Gleaming Glass-Spoked Wheel Display Stands (`lm_ring`, 1x2) & Forged Brass Bike-Rack Rails (`lm_railing_*`)!
    put_if('lm_ring', 9, 8)              # South showroom bike-rack glass-spoked wheel display stand A!
    put_if('lm_ring', 12, 8)             # South showroom bike-rack glass-spoked wheel display stand B!
    # Forged brass bike-rack stanchions neatly framing the fitting bay (x=10..11, y=9) + bollards (zero floating glitches!)
    m.over.append((1, 10, 9, P1('lm_railing_w')))
    m.over.append((1, 11, 9, P1('lm_railing_e')))
    m.taken[9, 10] = True; m.taken[9, 11] = True
    put_if('lm_bollard', 8, 5)
    put_if('lm_bollard', 13, 5)
    put_if('lm_bench', 9, 10)            # Customer fitting & helmet bench in the sculpted south bay!
    put_if('lm_topiary', 12, 9)          # Sculpted boutique topiary framing SE showroom corner

    # ---- 6. East Recessed Mechanic Repair Bench Alcove (x=14..17, y=5..9) ----
    # Authentic bicycle craftsman workshop: workbench, precision spoke lathe, gearboxes, spare parts rack & cables!
    put_if('lm_desk', 15, 5)             # (15..16, 5) Mechanic repair workbench!
    put_if('lm_rack', 17, 4)             # (17, 4..5) Tall spare frames & parts shelving!
    put_if('lm_gen', 16, 7)              # (16..17, 7..8) Wheel-truing & spoke-tensioning machine!
    put_if('lm_gearbox', 14, 5)          # Hub & drivetrain gearbox stand!
    put_if('lm_gearbox', 15, 8)          # Spare transmission block!
    put_if('lm_junction_on', 14, 9)      # Glowing amber workshop power console!
    m.over.append((2, 15, 6, P1('lm_cables')))  # Floor air-hose & power cables in the mechanic bay!
    put_if('lm_lamp_on', 14, 8)          # Warm mechanic work-light!

    # ---- 7. Warm Boutique Showroom Lighting: Chandeliers, Skylight Shafts & Golden Glow Pools! ----
    m.stamps.append(('lm_chand', 5, 5))   # Crystal chandelier over West Reception & Entrance!
    m.stamps.append(('lm_chand', 10, 5))  # Crystal chandelier crowning Central Flagship Cycle Podium!
    m.stamps.append(('cv_shaft', 10, 5))  # Sunlit skylight beam illuminating the Flagship Cycle Podium!
    for gx, gy in ((5, 6), (10, 6), (11, 6), (15, 6), (10, 8)):
        m.stamps.append(('pf_glow', gx, gy))

    m.paint()

    # ---- 8. Post-Paint Multi-Zone Showroom Floor Craft (ZERO blinding teal checkerboard!) ----
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    plazas = [P1('lm_plaza0'), P1('lm_plaza1')]
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] != '.' or m.cliff[y, x]:
                continue
            if x >= 14:
                # East Mechanic Repair Alcove: sleek dark obsidian slate & riveted steel workshop floor!
                m.L[0, y, x] = P1('lm_grate') if (x == 15 and 6 <= y <= 8) else P1('Z_f%d' % ((x * 3 + y) % 4))
            elif 8 <= x <= 13:
                # Central Flagship Cycle Showroom: luminous warm cream limestone framed by inlaid brass border!
                m.L[0, y, x] = plazas[(x + y) & 1]
            else:
                # West Reception Boutique: pale ashlar outer perimeter + warm cream marble center!
                perim = (x <= 2 or y == 8)
                m.L[0, y, x] = paves[(x * 3 + y * 5) % 4] if perim else plazas[(x + y) & 1]

    # Glowing Cyan-Brass Floor Inlay framing the Central Flagship Showcase Podium (x=8..13, y=6..9)
    # + Inlaid Golden Spoked-Wheel Sunburst Mosaic (`lm_sun`) crowning the showroom center (x=8..12, y=6..9)!
    sun_L = CK.STAMPS['lm_sun']['layers'][0]
    for dy in range(5):
        for dx in range(5):
            xx, yy = 8 + dx, 5 + dy
            if 6 <= yy <= 9 and 8 <= xx <= 13 and m.cls[yy, xx] == '.' and not m.cliff[yy, xx]:
                t = sun_L[dy][dx]
                if t:
                    m.L[0, yy, xx] = t
    for x in range(9, 13):
        if m.cls[6, x] == '.':
            m.L[0, 6, x] = P1('lm_inlay_h')
        if m.cls[9, x] == '.':
            m.L[0, 9, x] = P1('lm_inlay_h')
    for y in (7, 8):
        m.L[0, y, 8] = P1('lm_inlay_v')
        m.L[0, y, 13] = P1('lm_inlay_v')
    m.L[0, 6, 8] = P1('lm_inlay_se')
    m.L[0, 6, 13] = P1('lm_inlay_sw')
    m.L[0, 9, 8] = P1('lm_inlay_ne')
    m.L[0, 9, 13] = P1('lm_inlay_nw')

    # Meridian Workshop threshold power conduit into East Repair Bay
    m.L[0, 7, 14] = P1('lm_strip_h_on')
    m.L[0, 7, 15] = P1('lm_strip_h_on')

    # Royal Crimson Gala Welcome Carpet Runner from Exit (6,9) straight into Reception & Showroom (x=5..7, y=6..9)!
    for y in range(6, 10):
        for x in (5, 6, 7):
            if m.cls[y, x] == '.':
                part = ('n' if y == 6 else 's' if y == 9 else '') + ('w' if x == 5 else 'e' if x == 7 else '')
                m.L[0, y, x] = P1('lm_carpet_' + (part or 'c'))

    PG.guard(m.L, 60)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '187.npy'), m.L.astype(np.int16))

    # Preserve exact 2 HEAD events verbatim!
    spec_path = os.path.join(SPEC_DIR, '187_glide_cycles.yaml')
    old_spec = yaml.safe_load(open(spec_path))
    new_spec = {
        'id': 187,
        'name': old_spec['name'],
        'parent': old_spec['parent'],
        'metadata': old_spec['metadata'],
        'bgm': old_spec.get('bgm', ''),
        'tone': [8, 4, -6, 0],
        'raw': 'data/raw/187.npy',
        'tileset': 60,
        'events': old_spec['events'],
    }
    header = "# GENERATED by mapgen/layouts/wave8_story_craft.py (Wave 8 Map Craft): Glide Cycles (187).\n"
    open(spec_path, 'w').write(header + yaml.safe_dump(new_spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f"Wrote data/raw/187.npy {m.L.shape} and updated {spec_path}")
    return m.L


def main(which=None):
    sel = set(str(w) for w in (which or []))
    builders = [
        ('285', build_285),
        ('547', build_547),
        ('608', build_608),
        ('183', build_183),
        ('187', build_187),
    ]
    for mid, fn in builders:
        if not sel or mid in sel:
            fn()


if __name__ == '__main__':
    main(sys.argv[1:])
