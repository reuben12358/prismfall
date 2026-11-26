#!/usr/bin/env python3
"""layouts/wallshadow_row.py — Map 594: Wallshadow Row (150x80, tileset 60 PF Rejuv Lumen, field MEADOW).

The Crown Road running round the south foot of the towering white-grey Crownwall cliffs:
  - Double-tiered sheer white-grey Crownwall chalk cliffs (ht=3 & ht=2, kit `shc`) running organically across the
    north horizon, casting cool shadow over hedged Elowen barley/meadow farms, parted only at the Kingsmead Pass
    (north, guarded -> 756 by Tithe-reeve).
  - Seamless East continuity with built Map 593 (The Arc-Lamp Mile): arrival (148,40) facing left, wide paved
    Crown Road return warp (149, 38..42) -> 593 (1,20) right.
  - Paved Crown Road curving organically west with Milestones XVII & XVIII ("XVIII. SOUTHGATE. Crownhaven: no road."),
    Accord Tithe Barns with golden hayricks & fenced paddocks, The Four Ways Inn & 4-Kingdom Signpost (with its eerie
    blank 5th arm pointing straight at the Crownwall!) at the west crossroads, Southgate Shrine (stone chapel with
    inspectable 18+1 window, Prayer Board "and keep the One", & Shrine-keeper), and the hidden Shepherd's Track
    climbing the Crownwall foot to a bricked-up Accord cave (pf_minemouth + loose bricks + hidden Revive!).
  - 4 Guarded Crossroads Exits (pbRgssExists? -> 0 WARN) with canon roadblock NPCs:
      * West (Four Ways): 595 Coppice Ride & closed 681 Prism Falls (Royal Forester: "Pass, or no passage")
      * North: closed 756 Kingsmead gate (Tithe-reeve: "Nobody past the reeve without a seal")
      * South-East: chained 672 Long Drop lift-tower over Nadir chasm (Lift Guard: "Gala week. Nobody's going down")
      * East/NE spur: 602 Candle Down (Road-mender: "Back in a month since spring")
  - ALL 5 confirmed PBS trainers from pbs/trainers.txt (# Map 594 Wallshadow Row):
      AROMALADY Linnet, YOUNGSTER Hodge, LASS Marigold, TAMER Hob, TWINS Meg & Peg (double battle)
    plus 4 thematic item pickups (SUPERPOTION, GREATBALL, MIRACLESEED, hidden REVIVE).

Canon: design/WORLD.md:490-496, story/24_SCRIPT_CH5.md:213-282, pbs/trainers.txt (# Map 594).

Run:
    /usr/bin/python3 -I mapgen/layouts/wallshadow_row.py
"""
import os
import sys
import random
from collections import deque
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rkit as K
from rkit import P1, STAMPS
import lumenkit as LK
from lumenkit import City
import craftkit as CK
import rcompose as RC
import render as R
import passguard as PG
from terrain import vnoise, autotile_shape

TID = 60


def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map without emitting RMXP code-201 (keeps build.py at 0 WARN)."""
    dir_num = {'down': 2, 'left': 4, 'right': 6, 'up': 8}[direction]
    ruby = (
        'pbFadeOutIn do\n'
        '  $game_temp.player_new_map_id = %d\n'
        '  $game_temp.player_new_x = %d\n'
        '  $game_temp.player_new_y = %d\n'
        '  $game_temp.player_new_direction = %d\n'
        '  $scene.transfer_player\n'
        'end' % (map_id, tx, ty, dir_num)
    )
    return [{'if': 'pbRgssExists?("Data/Map%03d.rxdata")' % map_id,
             'then': [{'script': ruby}],
             'else': [blocked_text]}]


def _npc(at, name, sprite, lines, d='down', move='fixed', again=None):
    pages = [{'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(lines)}]
    if again:
        pages[0]['commands'] = pages[0]['commands'] + [{'selfswitch': ['A', True]}]
        pages.append({'cond': {'self': 'A'}, 'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(again)})
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': pages}


def _trainer(at, cls, name, intro, after, d='down', sight=4, rules=None):
    ev = {
        'type': 'trainer',
        'at': list(at),
        'sight': sight,
        'dir': d,
        'sprite': 'trainer_' + cls,
        'trainer': [cls, name],
        'intro': intro,
        'after': after,
    }
    if rules:
        ev['rules'] = list(rules)
    return ev


def _sign(at, name, text):
    return {'type': 'sign', 'name': name, 'at': list(at), 'post': False, 'text': text}


def _item(at, it, name, hidden=False):
    e = {'type': 'item', 'at': list(at), 'item': it, 'name': name}
    if hidden:
        e['hidden'] = True
    return e


def _smooth_blob(mask, passes=2):
    out = mask.copy()
    for _ in range(passes):
        pad = np.pad(out, 1, constant_values=False)
        n8 = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1]
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - out
        out = (out & (n8 >= 3)) | (~out & (n8 >= 5))
    return out


def _place_stamp_over(m, name, x, y, base_z=1, top_z=2, top_rows=0, solid=True):
    L = STAMPS[name]['layers']
    h, w = len(L[0]), len(L[0][0])
    for dy in range(h):
        for dx in range(w):
            if not m.inb(x + dx, y + dy):
                continue
            for sz_i in (0, 1, 2):
                t = int(L[sz_i][dy][dx])
                if t:
                    tz = top_z if (dy < top_rows or sz_i == 2) else base_z
                    m.over.append((tz, x + dx, y + dy, t))
            if solid:
                m.taken[y + dy, x + dx] = True


def _paint_woods_custom(m, palettes, seed=5941):
    """Multi-species interlocking Elowen forest canopy lattice (craftkit.SPECIES)."""
    rng = random.Random(seed)
    msk = (m.cls == 'T')
    tw, nt, nb = 3, 2, 2
    phase = rng.randrange(tw)
    for ty in range(-nt, m.H, 2):
        phase = (phase + rng.choice((1, 2))) % tw
        for tx in range(phase - tw, m.W, tw):
            foot = [(tx + dx, ty + nt + dy) for dx in range(tw) for dy in range(nb)]
            if not all(msk[y, x] for x, y in foot if m.inb(x, y)):
                continue
            if not any(m.inb(x, y) for x, y in foot):
                continue
            z = vnoise(tx, ty, seed, 14.0)
            pal = palettes[min(len(palettes) - 1, int(z * len(palettes) * 0.999))]
            sp = 'blossom' if rng.random() < 0.08 else rng.choices(list(pal), list(pal.values()))[0]
            top, bot, _ = CK.SPECIES[sp]
            for dy in range(nt):
                for dx in range(tw):
                    x, y = tx + dx, ty + dy
                    if m.inb(x, y) and top[dy][dx] and m.L[2, y, x] == 0:
                        m.L[2, y, x] = top[dy][dx]
            for dy in range(nb):
                for dx in range(tw):
                    x, y = tx + dx, ty + nt + dy
                    if m.inb(x, y) and bot[dy][dx]:
                        m.L[1, y, x] = bot[dy][dx]
                        m.taken[y, x] = True
    m.lattice = [CK.SPECIES[k] for k in CK.SPECIES]


def _bfs_check(m, start, targets, label):
    import build as B
    Lr = RC.resolve(m.L, m.tid).astype(np.int32)
    PG.guard(Lr, m.tid, [tuple(e['at']) for e in m.events if e and e.get('at')], label)
    ts = R.tilesets()[m.tid]
    H, W = m.H, m.W
    solid_ev = set()
    for e in m.events:
        if e.get('type') in ('npc', 'trainer'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if pg0.get('graphic') and not pg0.get('through'):
                solid_ev.add(tuple(e['at']))
    ok = np.array([[B.cell_passable(Lr, ts, x, y) for x in range(W)] for y in range(H)])
    sx, sy = start
    assert ok[sy, sx], '%s: start %s is NOT passable!' % (label, start)
    seen = {start}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and ok[ny, nx] and (nx, ny) not in solid_ev:
                seen.add((nx, ny))
                q.append((nx, ny))
    missing = []
    for name, (tx, ty), allow_adj in targets:
        if allow_adj:
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty), bool(ok[ty, tx])))
    print('%s BFS: %d walkable cells reached from %s; missing=%s' % (label, len(seen), start, missing))
    assert not missing, '%s unreachable targets: %s' % (label, missing)
    return seen


def _fix_all_autotiles(m):
    """Ensure every autotile slot lives on a single clean layer and matches NB2AUTO 100% (0 mismatches!)."""
    v_w = RC.vauto('rejuvenation', 'Still water', 0)   # slot 1 -> L0 ONLY
    v_W = RC.vauto('rejuvenation', 'Sea deep', 0)      # slot 2 -> L1 ONLY
    v_d = RC.vauto('pf', 'Gravel Spring', 0)           # slot 3 -> L1 ONLY
    v_u = RC.vauto('rejuvenation', 'DirtDark', 0)      # slot 4 -> L1 ONLY
    L = m.L
    H, W = m.H, m.W

    # 1. Remove any L1 autotiles that put_stamps()/over pushed down onto L0 (the root cause of NB2AUTO drift!)
    for y in range(H):
        for x in range(W):
            t0 = int(L[0, y, x])
            if v_W <= t0 < v_W + 48:
                L[0, y, x] = v_w
            elif (v_d <= t0 < v_d + 48) or (v_u <= t0 < v_u + 48):
                L[0, y, x] = K.SH_GRASS[y % 2][x % 2]
            t1 = int(L[1, y, x])
            if v_w <= t1 < v_w + 48:
                L[1, y, x] = 0

    # 2. Recompute exact NB2AUTO shapes independently on each layer/slot!
    for z, base in ((0, v_w), (1, v_W), (1, v_d), (1, v_u)):
        mask = (L[z] >= base) & (L[z] < base + 48)
        if not mask.any():
            continue
        for y, x in np.argwhere(mask):
            L[z, y, x] = base + autotile_shape(mask, x, y)

    # 3. Verify 0 NB2AUTO mismatches on resolved layers across ALL 7 autotile slots & all 3 layers!
    Lr = RC.resolve(L, m.tid).astype(np.int32)
    for z in range(3):
        for slot in range(1, 8):
            base = slot * 48
            mask = (Lr[z] >= base) & (Lr[z] < base + 48)
            if not mask.any():
                continue
            bad = 0
            for y, x in np.argwhere(mask):
                if int(Lr[z, y, x]) != base + autotile_shape(mask, x, y):
                    bad += 1
            assert bad == 0, 'Map 594 L%d slot%d still has %d NB2AUTO mismatches!' % (z, slot, bad)


def build_594():
    W, H = 150, 80
    if 'sh3' not in K.KITS:
        K.KITS['sh3'] = dict(K.KITS['sh'], rows=[K.KITS['sh']['rows'][0], K.KITS['sh']['rows'][1], K.KITS['sh']['rows'][3]])

    m = City(W, H, 594, base='.')
    m.auto = {
        'w': ('Still water', 'rejuvenation'),
        'W': ('Sea deep', 'rejuvenation'),
        'd': ('Gravel Spring', 'pf'),
        'u': ('DirtDark', 'rejuvenation'),
    }
    # ht=2 & ht=3 -> shc white Crownwall chalk; ht=1 -> sh3 Elowen earth terraces; ht=0 -> cvL dark basalt Nadir chasm rim!
    m.kit = {0: 'cvL', 1: 'sh3', 2: 'shc', 3: 'shc', 'default': 'shc'}
    m.STAIRS = K.STAIRS_STONE
    m.grass_var = True
    m.gv_dark = 0.54

    # ---- 1. TOWERING WHITE-GREY CROWNWALL CLIFFS (Double-Tiered Sheer Chalk Wall + Solid Accord Cave Outcrop!) ----
    # Aligned cleanly with the three ht=1 terraces below (ZERO brown sh3 lip colliding under white shc chalk!)
    wall_segments_h2 = [
        (0, 16, 12), (16, 27, 14), (27, 40, 13),
        # GAP at x=40..47 -> Kingsmead Pass through the Crownwall (guarded 756)!
        (48, 59, 15), (59, 66, 12), (66, 70, 14), (70, 78, 15), (78, 83, 14), (83, 95, 16),
        (95, 100, 13), (100, 112, 14), (112, 124, 15), (124, 138, 13), (138, 150, 11),
    ]
    for x0, x1, ybot in wall_segments_h2:
        for y in range(0, ybot):
            for x in range(x0, x1):
                m.ht[y, x] = 2

    # Second towering upper Crownwall peak ridge (ht=3, shc) stepped organically behind ht=2
    wall_segments_h3 = [
        (0, 18, 6), (18, 38, 8),
        (50, 64, 8), (64, 84, 7), (84, 106, 9), (106, 130, 7), (130, 150, 6),
    ]
    for x0, x1, ybot in wall_segments_h3:
        for y in range(0, ybot):
            for x in range(x0, x1):
                m.ht[y, x] = 3

    # ---- 2. Rolling Elowen Terraces (ht=1, sh3 warm earthen cliffs — seamlessly backing right into ht=2 chalk!) ----
    # (a) NW Prism Falls Bluff (x=0..27, meeting ht=2 with ZERO ht=0 trench -> ZERO brown north lip under chalk!)
    for y in range(10, 28):
        for x in range(0, 27):
            if m.ht[y, x] == 0:
                m.ht[y, x] = 1
    # (b) Central Shepherd's Track Shoulder (x=66..83, meeting ht=2 cleanly -> Accord Cave embeds flush in chalk!)
    for y in range(11, 24):
        for x in range(66, 83):
            if m.ht[y, x] == 0:
                m.ht[y, x] = 1
    # (c) NE Wallshadow Woodland Knoll (x=100..124, meeting ht=2 cleanly -> ZERO brown north lip under chalk!)
    for y in range(11, 25):
        for x in range(100, 124):
            if m.ht[y, x] == 0:
                m.ht[y, x] = 1

    # Stone stairs connecting ht=1 terraces cleanly to the valley floor!
    m.stairs(23, 27, w=3, n=3, kind='stone', c='d')     # NW Prism Falls stair (x=23..25, y=27..29 -> lands y=30)
    m.stairs(73, 23, w=3, n=3, kind='stone', c='u')     # Shepherd's Track stair (x=73..75, y=23..25 -> lands y=26)
    m.stairs(110, 24, w=3, n=3, kind='stone', c='d')    # NE Woodland Knoll stair (x=110..112, y=24..26 -> lands y=27)

    # ---- 3. Organic Border Woodlands, Alpine Crownwall Crest & Rich Interior Groves (ZERO bare deserts!) ----
    # Dense interlocking alpine canopy on upper Crownwall crest (staying 2 rows back from every chalk lip -> ZERO clip!)
    for x in range(W):
        if 39 <= x <= 48:
            continue
        for y in range(0, 7):
            if m.ht[y, x] == 3 and y + 2 < H and m.ht[y + 1, x] == 3 and m.ht[y + 2, x] == 3:
                m.cls[y, x] = 'T'

    # Alpine woodland pockets on mid-Crownwall ledges (ht=2, staying 2 rows clear of south chalk lip -> ZERO clip!)
    for cx, cy, rx, ry, sd in (
        (9, 9, 5.5, 1.8, 61), (26, 10, 4.8, 1.8, 62), (55, 11, 4.8, 1.8, 63),
        (75, 10, 5.2, 1.8, 64), (90, 12, 5.2, 1.8, 65), (118, 11, 6.0, 2.0, 66),
        (134, 9, 4.8, 1.8, 67),
    ):
        for y in range(max(0, int(cy - ry - 1)), min(H, int(cy + ry + 2))):
            for x in range(max(0, int(cx - rx - 1)), min(W, int(cx + rx + 2))):
                if (m.ht[y, x] == 2 and y + 2 < H and m.ht[y + 1, x] == 2 and m.ht[y + 2, x] == 2
                        and not (38 <= x <= 49)):
                    q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                    if q <= 1.0 + 0.35 * (vnoise(x, y, 5940 + sd, 3.0) - 0.5):
                        m.cls[y, x] = 'T'

    # West woodland border (leaving Prism Falls road y=20..26 & Coppice Ride y=38..45 wide open!)
    for y in range(13, H):
        if (19 <= y <= 26) or (37 <= y <= 45):
            continue
        depth = int(6.2 + 3.6 * vnoise(0, y, 5943, 10.0))
        for x in range(min(W, depth)):
            m.cls[y, x] = 'T'

    # East woodland border (leaving Candle Down spur y=19..26 & Arc-Lamp Mile arrival y=36..45 wide open!)
    for y in range(12, H):
        if (18 <= y <= 26) or (36 <= y <= 45):
            continue
        depth = int(6.0 + 4.2 * vnoise(149, y, 5944, 10.0))
        if y >= 52:
            depth = int(10.0 + 4.0 * vnoise(149, y, 5945, 9.0))
        for x in range(W - depth, W):
            m.cls[y, x] = 'T'

    # Lush undulating South Woodland border + dense wooded crag headlands wrapping BOTH sides of the Nadir Chasm!
    for x in range(W):
        if 111 <= x <= 135:
            continue
        base_d = 7.4 + 4.8 * vnoise(x, 79, 5946, 14.0) + 2.4 * vnoise(x, 70, 5948, 7.0)
        if 56 <= x <= 74:
            base_d = min(base_d, 6.2)   # keep southern brook basin & Great Ball meadow clear
        if 103 <= x <= 111 or 135 <= x <= 143:
            base_d = max(base_d, 13.0)  # deep dark woodland promontories framing BOTH chasm flanks!
        depth = int(base_d)
        for y in range(H - depth, H):
            m.cls[y, x] = 'T'

    # Rich interlocking Elowen woodland groves breaking up EVERY meadow sector (including SW, South-Central, SE, NE!)
    for cx, cy, rx, ry, sd in (
        # North-of-Road shadow copses
        (33, 21, 5.8, 4.8, 11), (57, 19, 4.8, 3.8, 12), (92, 20, 5.4, 4.0, 13), (129, 20, 5.2, 4.4, 14),
        (34, 32, 4.4, 3.4, 20), (104, 33, 4.8, 3.6, 19), (123, 28, 3.8, 2.8, 21), (134, 26, 3.6, 2.6, 22),
        # SW Orchard & Meadow woodland groves (cures 95% & 85% bare SW blocks!)
        (14, 57, 5.8, 4.6, 15), (14, 67, 5.4, 4.2, 23), (30, 64, 5.6, 4.4, 24), (39, 61, 5.8, 4.8, 16),
        # South-Central Brook & Pond-Bank groves (cures 60-77% bare south-central blocks!)
        (48, 63, 4.8, 4.2, 25), (81, 61, 4.6, 3.8, 26), (92, 62, 6.6, 5.2, 17),
        (54, 51, 3.4, 2.6, 27), (80, 50, 3.4, 2.6, 28),
        # SE Southgate Sanctuary & Timber-Yard groves (cures 55-79% bare SE blocks!)
        (104, 66, 5.0, 4.2, 29), (129, 57, 5.6, 4.8, 18), (134, 65, 5.2, 4.2, 30),
    ):
        m.blob(cx, cy, rx, ry, 'T', seed=5940 + sd, rough=0.56, only='.')

    # ---- 4. JAGGED DARK-BASALT NADIR CHASM ESCARPMENT (ht=-1, kit[0]=cvL!) & N-S HOURGLASS ELOWEN POND! ----
    # (a) Stepped dark-basalt chasm plunging below Long Drop gantry (y=72 is cvL lip, y=73..74 sheer rock face, y=75..79 abyss!)
    #     Steps are >=2 tiles wide so cvL renders crisp basalt corner cliffs with ZERO flat grass touching starry void!
    for x in range(111, 136):
        if 115 <= x <= 131:
            rim_y = 73
        elif x in (113, 114, 132, 133):
            rim_y = 74
        else:
            rim_y = 75
        for y in range(rim_y, H):
            m.ht[y, x] = -1
            m.cls[y, x] = 'x'
    # Wrap dark woodland right up to the east/west basalt chasm walls (x=108..112, y=71..79 & x=134..138, y=71..79)
    for y in range(70, H):
        for x in range(106, 111):
            if m.ht[y, x] == 0:
                m.cls[y, x] = 'T'
        for x in range(136, 141):
            if m.ht[y, x] == 0:
                m.cls[y, x] = 'T'

    # (b) Graceful North-South Hourglass Elowen Brook Pond (x=57..73, y=51..69)!
    #     North basin (64,54) + South basin (65,65) joined by narrow bridge channel (63..67, 56..63).
    #     Solid mainland grass on BOTH west (x<=62, y=58..61) & east (x>=68, y=58..61) -> genuine shoreline-anchored bridge!
    pond = np.zeros((H, W), bool)
    for cx, cy, rx, ry, sd in ((64, 54, 6.6, 3.6, 31), (65, 65, 7.2, 3.7, 32)):
        for y in range(49, 71):
            for x in range(53, 77):
                q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if q <= 1.0 + 0.30 * (vnoise(x, y, 5940 + sd, 3.5) - 0.5):
                    pond[y, x] = True
    # Clean 5-wide water channel joining north & south basins right beneath the timber footbridge!
    pond[55:64, 63:68] = True
    # Keep west & east bridge banks (y=58..61) solid mainland grass so bridge meets REAL shoreline (ZERO floating islands!)
    pond[58:62, :63] = False
    pond[58:62, 68:] = False
    pond = _smooth_blob(pond, passes=1)
    # Re-assert crisp bridge channel & mainland banks after smoothing
    pond[57:63, 63:68] = True
    pond[58:62, 60:63] = False
    pond[58:62, 68:71] = False
    m.cls[pond] = 'w'
    # Deep water strictly inside wide open basins (never under bridge railings y=58..61!)
    p_pad = np.pad(pond, 2, constant_values=False)
    deep_p = pond.copy()
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            deep_p &= p_pad[2 + dy:2 + dy + H, 2 + dx:2 + dx + W]
    deep_p[57:63, :] = False
    m.cls[deep_p] = 'W'

    # ---- 5. THE PAVED CROWN ROAD (SWEEPING NATURAL S-CURVE!), 4 CROSSROADS BRANCHES & COUNTRY LANES ----
    crown_pts = [
        (0, 41), (14, 41), (26, 42), (38, 40), (50, 38), (64, 37), (78, 38),
        (94, 41), (110, 44), (126, 42), (138, 40), (149, 40),
    ]
    m.lane(crown_pts, c='p', w=5.4, seed=5951, only='T.tdu', wobble=0.14)
    m.lane(crown_pts, c='q', w=3.0, seed=5952, only='p', wobble=0.10)
    # Crisp exact East Arrival apron seamlessly welded into S-curve 'q' (ZERO stray vertical 'p' kerb stripe at x=138!)
    m.rect(138, 38, 12, 5, 'p')
    m.rect(135, 39, 15, 3, 'q')
    # Crisp exact West Four Ways apron seamlessly welded into S-curve 'q' (ZERO stray vertical 'p' stripe at x=11!)
    m.rect(0, 39, 12, 5, 'p')
    m.rect(0, 40, 15, 3, 'q')

    # Branch 1: North Kingsmead Accord Road (x=42..46, y=0..40 -> guarded 756!)
    m.rect(41, 0, 6, 17, 'p')
    m.rect(42, 0, 4, 17, 'q')
    m.lane([(44, 39), (44, 27), (44, 15)], c='p', w=4.0, seed=5953, only='T.tdu', wobble=0.15)
    m.lane([(44, 39), (44, 27), (44, 15)], c='q', w=2.0, seed=5954, only='p', wobble=0.10)

    # Branch 2: NW Prism Falls Road (climbing up stair (23..25, 27..29) onto NW bluff -> guarded 681!)
    m.lane([(24, 41), (24, 34), (24, 30)], c='d', w=2.8, seed=5955, only='T.t', wobble=0.10)
    m.lane([(24, 27), (19, 23), (10, 23), (0, 23)], c='d', w=2.8, seed=5956, only='T.t', wobble=0.15)
    m.rect(0, 21, 8, 4, 'd')

    # Branch 3: South-East Road past Southgate Shrine down to The Long Drop Lift-Tower (guarded 672!)
    m.lane([(110, 44), (112, 54), (116, 60), (121, 66), (122, 71)], c='p', w=3.6, seed=5957, only='T.tdu', wobble=0.18)
    m.lane([(110, 44), (112, 54), (116, 60), (121, 66), (122, 71)], c='q', w=1.8, seed=5958, only='p', wobble=0.10)
    # Dark soot-stone lift-tower gantry platform at (116..129, 67..72) cantilevering over the cvL basalt chasm!
    m.rect(116, 67, 14, 6, 'l')
    m.rect(119, 68, 7, 4, 'p')

    # Branch 4: NE Candle Down Spur (east fork off Crown Road -> guarded 602!)
    m.lane([(126, 42), (132, 33), (138, 24), (149, 23)], c='p', w=3.8, seed=5959, only='T.tdu', wobble=0.16)
    m.lane([(126, 42), (132, 33), (138, 24), (149, 23)], c='q', w=1.8, seed=5960, only='p', wobble=0.10)
    m.rect(142, 21, 8, 4, 'p')
    m.rect(142, 22, 8, 2, 'q')

    # Country Farm & Meadow Footpaths (Northern Wallshadow Tithe Barns, Shepherd's Track, South Brook Loop!)
    m.lane([(46, 35), (55, 34), (65, 33), (74, 28), (74, 26)], c='u', w=2.2, seed=5961, only='T.t', wobble=0.20)
    m.lane([(74, 22), (74, 19), (74, 17)], c='u', w=2.0, seed=5962, only='T.t', wobble=0.12)  # Shepherd's Track to embedded Accord Cave!
    m.lane([(65, 33), (78, 34), (88, 35), (96, 36), (105, 30), (111, 27)], c='d', w=2.2, seed=5963, only='T.t', wobble=0.18)
    m.lane([(111, 23), (111, 19), (117, 19)], c='u', w=2.0, seed=5964, only='T.t', wobble=0.15)  # NE Knoll glade path!
    # Scenic gravel lane to Four Ways well & roadside coppice
    m.lane([(25, 35), (30, 35), (36, 37)], c='d', w=2.0, seed=5969, only='T.t', wobble=0.15)
    # Four Ways Inn yard (starts at y=39 cleanly below doors at y=38!) & SW orchard meadow track
    m.rect(12, 39, 10, 2, 'd')
    m.lane([(28, 45), (30, 51), (24, 58), (22, 65)], c='d', w=2.2, seed=5965, only='T.t', wobble=0.20)
    # South Brook & Meadow Loop approaching bridge cleanly over solid mainland banks (61..62, 59..60) & (68..69, 59..60)!
    m.lane([(48, 41), (50, 51), (54, 58), (61, 59), (62, 59)], c='u', w=2.2, seed=5966, only='T.t', wobble=0.18)
    m.lane([(68, 59), (72, 59), (79, 55), (84, 49), (86, 43)], c='u', w=2.2, seed=5967, only='T.t', wobble=0.18)
    m.lane([(74, 59), (77, 65), (76, 70)], c='u', w=2.0, seed=5968, only='T.t', wobble=0.18)
    # Southgate Shrine courtyard apron (x=104..115, y=55..59)
    m.rect(104, 55, 11, 4, 'p')
    m.rect(106, 56, 7, 2, 'q')

    # Slender 5x2 Warm-Timber Footbridge spanning the narrow N-S water channel (x=63..67, y=59..60)!
    # West bank (61..62, 59..60) & east bank (68..69, 59..60) are REAL mainland grass + dirt path (ZERO floating gravel!)
    for y in (59, 60):
        for x in (61, 62, 68, 69):
            m.cls[y, x] = 'u'
            m.keep_clear.add((x, y))
    for bx, by in ((62, 58), (62, 61), (68, 58), (68, 61)):
        m.cls[by, bx] = '.'
        m.keep_clear.add((bx, by))
    bridge_cells = [(x, y) for y in (59, 60) for x in range(63, 68)]
    for bx, by in bridge_cells:
        m.cls[by, bx] = '.'
        m.keep_clear.add((bx, by))

    # ---- 6. LUSH IRREGULAR MULTI-LOBE TALL-GRASS ENCOUNTER GLADES (organic curved lobes — ZERO boxy rectangles!) ----
    grass_lobes = [
        # West & SW Orchard / Four Ways Meadow pockets (dresses SW 10..29, 50..69!)
        (12, 48, 4.4, 3.2, 41), (19, 50, 3.8, 2.8, 42),
        (21, 61, 3.8, 3.0, 60), (26, 56, 3.8, 2.8, 61), (17, 65, 3.6, 2.6, 62),
        (33, 50, 4.5, 3.4, 43), (39, 53, 4.0, 3.0, 44), (36, 28, 3.6, 2.6, 58),
        # Wallshadow Shaded Hedgerow Barley/Herb Fields (north of Crown Road!)
        (61, 28, 4.2, 3.2, 45), (66, 29, 3.8, 2.8, 46),
        (76, 30, 4.2, 3.0, 47), (80, 32, 3.4, 2.6, 48),
        (106, 36, 3.8, 2.6, 63), (117, 19, 4.2, 2.8, 49), (121, 33, 4.5, 3.2, 50), (114, 33, 3.6, 2.8, 59),
        # Central-South Brook & Pond-Rim Meadows (dresses 40..89, 44..70!)
        (45, 47, 3.8, 2.8, 64), (55, 46, 4.4, 3.2, 51), (63, 46, 3.8, 2.8, 52),
        (54, 62, 3.8, 2.8, 65), (56, 67, 4.0, 2.8, 66), (72, 70, 3.6, 2.6, 67),
        (84, 59, 4.2, 3.0, 53), (95, 55, 4.2, 3.2, 54),
        # SE Southgate Memorial Meadow & East Arc-Lamp Organic Glades (broken up — ZERO 8x4 box at 134..141!)
        (106, 62, 3.8, 2.8, 68), (113, 62, 3.4, 2.6, 69),
        (123, 52, 4.2, 3.2, 55), (132, 49, 3.8, 2.8, 56), (122, 62, 3.6, 2.6, 70),
        (132, 33, 3.2, 2.4, 57), (140, 32, 2.8, 2.2, 71), (135, 21, 3.2, 2.4, 72),
    ]
    tmask = np.zeros((H, W), bool)
    for cx, cy, rx, ry, sd in grass_lobes:
        for y in range(max(0, int(cy - ry - 2)), min(H, int(cy + ry + 3))):
            for x in range(max(0, int(cx - rx - 2)), min(W, int(cx + rx + 3))):
                if m.cls[y, x] != '.':
                    continue
                if m.ht[y, x] >= 2:
                    continue
                q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if q <= 1.0 + 0.56 * (vnoise(x, y, 5970 + sd, 2.5) - 0.5):
                    tmask[y, x] = True
    tmask = _smooth_blob(tmask, passes=1) & (m.cls == '.') & (m.ht <= 1)
    road = np.isin(m.cls, ['p', 'q', 'r', 'l', 'd', 'u', 'w', 'W', 'x'])
    rpad = np.pad(road, 1, constant_values=False)
    near_r = np.zeros_like(road)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            near_r |= rpad[1 + dy:1 + dy + H, 1 + dx:1 + dx + W]
    tmask &= ~near_r
    # Extra organic pinch along East Approach (x=134..141, y=34..37) so it reads as soft curved glades, never a box!
    for x in range(135, 139):
        tmask[35:38, x] = False
    m.cls[tmask] = 't'

    # ---- 7. ARCHITECTURAL LANDMARKS (100% Clean Transparent Silhouettes, ZERO copy-paste, ZERO black halos!) ----
    # (a) THE FOUR WAYS INN (West Crossroads: sp_inn 6x8 + adjoining sp_tav 5x7 — cleanly below NW bluff cliff!)
    m.put('sp_inn', 11, 31, force=True)      # door at (13, 38) opening onto inn courtyard y=39!
    m.put('sp_tav', 17, 32, force=True)      # adjoining stable/taproom wing (door at (18, 38))

    # (b) ACCORD TITHE BARNS & SHADOW FARMSTEAD (distinct silhouettes across the valley!)
    m.put('wh_d', 50, 24, force=True)        # West Accord Tithe Barn (7x9, stone & shingle, door (53, 32))
    m.put('gl_shed', 57, 27, force=True)     # West Grain & Tithe Scale Shed (4x6)
    m.put('th_y', 69, 44, force=True)        # Hedged Barley Farmhouse (7x6, golden ochre gable, door (71, 49))
    m.put('wh_b', 83, 26, force=True)        # East Accord Tithe Barn (7x8, warm ochre timber, door (86, 33))
    m.put('wh_c', 90, 27, force=True)        # East Dark-Timber Harvest Barn (6x7, door (92, 33))
    m.put('th_w', 95, 46, force=True)        # Southgate Sexton's Cottage (6x6, timber-framed)

    # (c) SOUTHGATE SHRINE (South Junction: wh_e 8x8 stone-and-slate Accord chapel!)
    m.put('wh_e', 105, 48, force=True)       # door (108, 55) opening onto Southgate Shrine stone courtyard y=56..58!

    # (d) KINGSMEAD PASS GATE TOWERS framing the North Crownwall Pass (x=38..48)!
    m.put('gt_tower', 38, 10, force=True)    # West Kingsmead Gate Bastion
    m.put('gt_tower', 47, 10, force=True)    # East Kingsmead Gate Bastion

    # (e) SECRET BRICKED-UP ACCORD CAVE EMBEDDED FLUSH INTO THE WHITE CHALK CROWNWALL CLIFF (73..75, 14..16)!
    _place_stamp_over(m, 'pf_minemouth', 73, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    # Authentic old Accord stone masonry walling up the lower cave mouth (replaces plastic sawhorse!)
    for bx, nm in ((73, 'nr_wall_w'), (74, 'nr_wall_m'), (75, 'nr_wall_e')):
        _place_stamp_over(m, nm, bx, 16, base_z=2, top_z=2, top_rows=1, solid=True)
    # White chalk boulders hugging both sides of the cave mouth directly into the chalk cliff!
    _place_stamp_over(m, 'ck_boulder', 71, 16, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'ck_boulder', 76, 16, base_z=1, top_z=1, top_rows=0, solid=True)

    # ---- 8. COMPOSED ELOWEN COUNTRYSIDE VIGNETTES, ENCLOSED HEDGEROW PADDOCKS, MILESTONES, LONG DROP ----
    # (a) Milestones XVII & XVIII + Four-Kingdom Signpost + Road Signs
    _place_stamp_over(m, 'pf_roadstone', 45, 41, base_z=1, top_z=2, top_rows=1, solid=True)   # Milestone XVII
    _place_stamp_over(m, 'pf_roadstone', 108, 40, base_z=1, top_z=2, top_rows=1, solid=True)  # Milestone XVIII
    _place_stamp_over(m, 'pf_signpost', 26, 44, base_z=1, top_z=2, top_rows=1, solid=True)    # Four-Kingdom Signpost!
    _place_stamp_over(m, 'pf_signpost', 142, 36, base_z=1, top_z=2, top_rows=1, solid=True)   # East Wallshadow Road Sign

    # (b) The Four Ways Inn Courtyard (mounting block, wagon & barrels cleanly pulled clear of wall/gravel!)
    _place_stamp_over(m, 'pf_stonebench', 15, 39, base_z=1, top_z=1, top_rows=0, solid=True)  # Juno's mounting block!
    _place_stamp_over(m, 'pf_wagon', 7, 35, base_z=1, top_z=2, top_rows=1, solid=True)        # Clear of sp_inn west wall!
    _place_stamp_over(m, 'pf_well', 27, 34, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'hb_barrels', 9, 37, base_z=1, top_z=2, top_rows=1, solid=True)      # Clear of gravel & inn wall!
    _place_stamp_over(m, 'pf_lantern', 11, 38, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_lantern', 22, 38, base_z=1, top_z=2, top_rows=2, solid=True)

    # (c) Accord Tithe Barns, SW Grazing Pasture, Farmhouse Yard & Hedged Barley Fields!
    for hx, hy in (
        (51, 35), (62, 31), (76, 47), (79, 32), (96, 33), (48, 49), (87, 49),
        (118, 35), (125, 35), (30, 36), (17, 61), (25, 62), (66, 47), (103, 35), (127, 61),
    ):
        if m.inb(hx + 1, hy + 1) and all(m.cls[hy + dy, hx + dx] == '.' and not m.taken[hy + dy, hx + dx] for dy in range(2) for dx in range(2)):
            _place_stamp_over(m, 'pf_hayrick', hx, hy, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_wagon', 58, 34, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_wagon', 81, 34, base_z=1, top_z=2, top_rows=1, solid=True)       # Pulled cleanly off Crown Road kerb into yard!
    _place_stamp_over(m, 'pf_wagon', 124, 59, base_z=1, top_z=2, top_rows=1, solid=True)      # Lift-Warden's timber wagon!
    _place_stamp_over(m, 'pf_well', 77, 45, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_sacks', 55, 32, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sacks', 89, 34, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sacks', 106, 34, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_boxes', 95, 35, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_boxes', 122, 57, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_barrels', 68, 49, base_z=1, top_z=2, top_rows=1, solid=True)

    # Rustic timber split-rail hedgerow paddock fences (north barns, SW pasture, east barley fields, timber yard!)
    fence_runs_h = [
        (49, 57, 43), (69, 79, 42), (83, 93, 45),
        (51, 59, 23), (82, 95, 25),
        (100, 108, 37), (114, 127, 38), (116, 128, 28),
        (120, 132, 46), (29, 38, 37),
        (12, 20, 60), (24, 31, 61), (120, 129, 63),
    ]
    for fx0, fx1, fy in fence_runs_h:
        for fx in range(fx0, fx1 + 1):
            if m.inb(fx, fy) and m.cls[fy, fx] == '.' and not m.taken[fy, fx] and m.ht[fy, fx] == 0:
                _place_stamp_over(m, 'wr_pal_h', fx, fy, base_z=1, top_z=1, top_rows=0, solid=True)
    fence_runs_v = [
        (49, 44, 48), (69, 43, 44), (114, 30, 37), (127, 30, 37), (29, 33, 36),
        (12, 61, 64), (100, 33, 36), (120, 58, 62),
    ]
    for fx, fy0, fy1 in fence_runs_v:
        for fy in range(fy0, fy1 + 1):
            if m.inb(fx, fy) and m.cls[fy, fx] == '.' and not m.taken[fy, fx] and m.ht[fy, fx] == 0:
                _place_stamp_over(m, 'wr_pal_v', fx, fy, base_z=1, top_z=1, top_rows=0, solid=True)

    # Elowen dry-stone low walls framing Southgate Memorial Garden, Farmhouse Pond Bank & Crown Road verges!
    stone_wall_runs = [
        (101, 106, 60), (110, 114, 60),        # Southgate Pilgrim Memorial Garden wall
        (58, 66, 49), (73, 78, 51),            # Barley Farmhouse & North Pond Bank stone wall
        (42, 47, 43), (59, 66, 41),            # Crown Road southern stone verge wall
    ]
    for sx0, sx1, sy in stone_wall_runs:
        for sx in range(sx0, sx1 + 1):
            if m.inb(sx, sy) and m.cls[sy, sx] == '.' and not m.taken[sy, sx] and m.ht[sy, sx] == 0:
                piece = 'nr_wall_w' if sx == sx0 else ('nr_wall_e' if sx == sx1 else 'nr_wall_m')
                _place_stamp_over(m, piece, sx, sy, base_z=1, top_z=1, top_rows=0, solid=True)

    # Rustic logs, stumps, pondside log benches & Southgate Memorial stone ring!
    for nm, px, py in (
        ('pf_logbench', 19, 63), ('pf_logbench', 55, 56), ('pf_logbench', 73, 56), ('pf_logbench', 105, 65),
        ('nt_log', 26, 67), ('nt_log', 51, 66), ('nt_log', 124, 55), ('nt_log', 132, 62), ('nt_log', 43, 58),
        ('nt_stump', 16, 63), ('nt_stump', 61, 69), ('nt_stump', 126, 56), ('nt_stump', 102, 62),
        ('nt_stonering', 107, 63),
    ):
        st = STAMPS[nm]
        if m.free(px, py, st['w'], st['h'], on='.'):
            _place_stamp_over(m, nm, px, py, base_z=1, top_z=2 if st['h'] > 1 else 1, top_rows=max(0, st['h'] - 1), solid=True)

    # (d) Southgate Shrine Stone Courtyard (twin stone shrines given 1 full tile breathing room clear of chapel eaves!)
    _place_stamp_over(m, 'pf_shrine', 102, 52, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_shrine', 114, 52, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_lantern', 104, 56, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_lantern', 113, 56, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 104, 59, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 112, 59, base_z=1, top_z=1, top_rows=0, solid=True)

    # (e) THE LONG DROP LIFT-TOWER into Nadir (gantry bars on L2 cleanly over cvL basalt cliff lip on L1 at y=72!)
    _place_stamp_over(m, 'lm_pylon', 117, 64, base_z=1, top_z=2, top_rows=3, solid=True)
    _place_stamp_over(m, 'hb_crane', 125, 65, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_bars_l', 121, 72, base_z=2, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bars_m', 122, 72, base_z=2, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bars_r', 123, 72, base_z=2, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_chain', 122, 73, base_z=2, top_z=2, top_rows=1, solid=True)      # Hanging over sheer basalt drop!
    for rx in range(115, 121):
        piece = 'lm_bollard' if rx in (115, 120) else 'lm_railing_m'
        _place_stamp_over(m, piece, rx, 72, base_z=2, top_z=2, top_rows=0, solid=True)
    for rx in range(124, 132):
        piece = 'lm_bollard' if rx in (124, 131) else 'lm_railing_m'
        _place_stamp_over(m, piece, rx, 72, base_z=2, top_z=2, top_rows=0, solid=True)
    # Stepped chasm flank guard bollards along the rocky precipice brink (x=113..114, 132..133 at y=73)!
    for rx, ry in ((113, 73), (114, 73), (132, 73), (133, 73)):
        _place_stamp_over(m, 'lm_bollard', rx, ry, base_z=2, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_boxes', 116, 68, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_lantern', 119, 67, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_lantern', 125, 69, base_z=1, top_z=2, top_rows=2, solid=True)

    # (f) Roadblock Barricades & Lanterns at Kingsmead Pass, Prism Falls Bluff & Candle Down Mending Site
    _place_stamp_over(m, 'pf_barricade', 42, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_barricade', 45, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_lantern', 41, 15, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_lantern', 46, 15, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_barricade', 143, 21, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_tools', 144, 24, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_wagon', 139, 26, base_z=1, top_z=2, top_rows=1, solid=True)

    # (g) Rich Gen 5 Woodland Groves, Orchard Trees & Nadir Chasm Pines (ZERO broken tr_teal; 2+ tiles clear of cliff lips!)
    grove_trees = [
        # Alpine Crownwall ledge pines cleanly behind white chalk cliff lips!
        ('tr_pine', 12, 7), ('tr_pine2', 31, 8), ('tr_pine', 60, 8), ('tr_pine2', 80, 9),
        ('tr_pine', 100, 9), ('tr_pine2', 114, 9), ('tr_pine', 135, 8),
        # Four Ways Inn & NW Prism Falls Bluff grove
        ('nt_blossom', 8, 28), ('tr_oak', 26, 28), ('nt_lime', 28, 30), ('tr_oak2', 8, 15), ('nt_blossom', 14, 16),
        ('nt_blossom', 31, 33), ('tr_oak', 37, 32), ('tr_pine', 18, 15),
        # Wallshadow Northern Farm Hedgerow trees + shoulder framing trees at shc/sh3 joints!
        ('tr_oak', 47, 25), ('nt_olive', 61, 20), ('tr_oak2', 64, 19), ('nt_lime', 65, 25), ('tr_oak2', 80, 25),
        ('tr_pine', 84, 19), ('nt_blossom', 96, 26), ('tr_oak', 98, 20),
        ('tr_oak', 102, 17), ('nt_blossom', 107, 17), ('nt_lime', 115, 16), ('tr_oak2', 121, 17),
        ('tr_oak', 101, 29), ('tr_pink', 107, 30), ('tr_pine', 132, 27), ('tr_oak2', 137, 29),
        # SW Orchard & Meadow Groves (eliminates bare SW desert!)
        ('tr_pink', 11, 61), ('nt_blossom', 19, 55), ('tr_oak', 24, 59), ('tr_oak2', 26, 65),
        ('tr_pink', 16, 66), ('tr_pine', 29, 58), ('nt_blossom', 26, 52), ('tr_oak', 33, 56),
        # South-Central Brook, Farmhouse & Pond-Rim Groves (eliminates bare south-central desert!)
        ('nt_lime', 44, 52), ('tr_oak2', 46, 57), ('tr_pine', 52, 54), ('tr_oak', 54, 65),
        ('nt_blossom', 67, 50), ('tr_oak', 74, 52), ('nt_blossom', 78, 52), ('tr_oak2', 82, 56),
        ('nt_olive', 87, 52), ('tr_pine2', 78, 66), ('tr_oak', 63, 69), ('tr_pink', 58, 69),
        ('tr_oak', 43, 44), ('tr_pine', 61, 42), ('nt_lime', 82, 43),
        # SE Southgate Shrine, Memorial Orchard & Nadir Chasm Promontory Pines (eliminates bare SE desert!)
        ('tr_oak2', 99, 57), ('tr_pink', 101, 61), ('nt_blossom', 109, 61), ('tr_pine', 113, 65),
        ('tr_oak', 106, 66), ('nt_blossom', 115, 55), ('tr_pink', 119, 48), ('tr_oak', 126, 48),
        ('tr_pine', 123, 64), ('tr_pine2', 130, 63), ('tr_pine', 111, 67), ('tr_pine2', 133, 66),
        ('nt_deadtree', 112, 68), ('nt_deadtree', 132, 68),
        # East Southgate & Arc-Lamp Border Grove (breaks up boxy east approach!)
        ('nt_lime', 134, 44), ('tr_pink', 136, 33), ('tr_oak', 131, 35), ('nt_blossom', 124, 25), ('tr_oak2', 129, 24),
    ]
    for kind, tx, ty in grove_trees:
        st = STAMPS[kind]
        if m.free(tx, ty, st['w'], st['h'], on='.'):
            m.stamp(kind, tx, ty, mark='B')

    # Clean Green Shoreline Reeds (ONLY nt_reed1 — NEVER corrupt pale-blue nt_reed0!) & Shallow-Water Irises (nt_lily)!
    for rx, ry in ((56, 54), (58, 57), (71, 55), (56, 64), (72, 64), (60, 68), (69, 68)):
        if m.inb(rx, ry) and m.inb(rx, ry - 1) and m.cls[ry, rx] == '.' and m.cls[ry - 1, rx] == '.' and not m.taken[ry, rx]:
            _place_stamp_over(m, 'nt_reed1', rx, ry - 1, base_z=1, top_z=2, top_rows=1, solid=True)
    # Place FULL 1x2 nt_lily ONLY on shallow 'w' water (NEVER on 'W' deep water -> ZERO water autotile breakage!)
    for lx, ly in ((59, 54), (69, 54), (61, 56), (60, 65), (70, 65), (66, 67)):
        if m.inb(lx, ly) and m.inb(lx, ly - 1) and m.cls[ly, lx] == 'w':
            m.over.append((1, lx, ly, 6852))
            m.over.append((2, lx, ly - 1, 6844))

    # Mossy Valley Boulders, White Crownwall Chalk Boulders & Dark Nadir Chasm Crags!
    for nm, bx, by in (
        # White chalk boulders hugging Crownwall ledges & shc/sh3 shoulder transitions
        ('ck_boulder', 64, 14), ('ck_boulder', 83, 17), ('ck_boulder', 98, 15), ('ck_boulder', 124, 16),
        ('ck_boulder', 19, 9), ('ck_boulder', 66, 9), ('ck_boulder', 98, 10), ('ck_boulder', 126, 10),
        # Dark crag boulders framing the Nadir chasm escarpment flanks
        ('dk_boulder', 113, 70), ('dk_boulder', 132, 70), ('dk_boulder', 115, 65), ('dk_boulder', 129, 65),
        # Scenic valley boulders across meadows, pond banks & road verges
        ('nt_boulder', 68, 18), ('nt_boulder', 79, 18), ('nt_boulder', 105, 20), ('nt_boulder', 35, 36),
        ('nt_boulder', 52, 62), ('nt_boulder', 75, 63), ('nt_boulder', 101, 63), ('nt_boulder', 136, 35),
        ('nt_boulder', 21, 67), ('nt_boulder', 43, 62), ('nt_boulder', 66, 51), ('nt_boulder', 124, 49),
    ):
        if m.free(bx, by, 2, 2, on='.'):
            m.stamp(nm, bx, by, mark='B')

    # Flowering Azaleas & Meadow Shrubs tucked into orchard, pond & roadside glades!
    for nm, ax, ay in (
        ('nt_azalea0', 15, 59), ('nt_azalea1', 23, 53), ('nt_azalea2', 28, 62), ('nt_azalea0', 103, 58),
        ('nt_azalea1', 113, 60), ('nt_azalea2', 59, 51), ('nt_azalea0', 71, 52), ('nt_azalea1', 64, 44),
        ('nt_azalea2', 45, 54), ('nt_azalea0', 84, 53), ('nt_azalea1', 122, 54), ('nt_azalea2', 105, 32),
        ('nt_shrub0', 12, 65), ('nt_shrub1', 27, 50), ('nt_shrub0', 51, 58), ('nt_shrub1', 74, 67),
        ('nt_shrub0', 108, 67), ('nt_shrub1', 128, 51), ('nt_shrub0', 137, 36), ('nt_shrub1', 62, 39),
    ):
        if m.free(ax, ay, 2, 2, on='.'):
            m.stamp(nm, ax, ay, mark='B')

    # ---- 9. EVENTS: Active Warp to 593, 4 Guarded Crossroads Exits, Canon NPCs, 5 PBS Trainers, 4 Items ----
    E = m.events

    # ACTIVE WARP: East Crown Road back to built Map 593 (The Arc-Lamp Mile -> (1,20) right!)
    for wy in (38, 39, 40, 41, 42):
        E.append({
            'type': 'warp',
            'name': 'To The Arc-Lamp Mile',
            'at': [149, wy],
            'to': {'map': 593, 'x': 1, 'y': 20, 'dir': 'right'},
            'se': 'Door exit',
        })

    # GUARDED CROSSROADS EXITS (pbRgssExists? -> 0 warnings!)
    # (1a) West (Four Ways): 595 Coppice Ride
    for wy in (39, 40, 41, 42, 43):
        E.append({
            'type': 'event',
            'name': 'To Coppice Ride',
            'at': [0, wy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    595, 108, 36, 'left',
                    "(The hazel-coppice gate west to Coppice Ride is latched while the woodwards clear felled brush. Not built yet.)"
                ),
            }],
        })
    # (1b) NW (Four Ways Bluff): 681 Prism Falls (closed Queen's road)
    for wy in (21, 22, 23, 24):
        E.append({
            'type': 'event',
            'name': 'To Prism Falls',
            'at': [0, wy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    681, 128, 40, 'left',
                    "(The Queen's road west toward Prism Falls & Verdance is closed without a Royal Forester's pass.)"
                ),
            }],
        })
    # (2) North (Crownwall Pass): 756 Kingsmead (closed Accord paddocks)
    for kx in (42, 43, 44, 45):
        E.append({
            'type': 'event',
            'name': 'To Kingsmead',
            'at': [kx, 1],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    756, 55, 86, 'up',
                    "(Kingsmead's Accord paddock gate is chained shut. Nobody passes the reeve without a Sovereign's seal.)"
                ),
            }],
        })
    # (3) South-East (Chained Lift-Tower): 672 The Long Drop into Nadir
    for lx in (121, 122, 123):
        E.append({
            'type': 'event',
            'name': 'To The Long Drop',
            'at': [lx, 71],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    672, 32, 4, 'down',
                    "(The great iron lift-cage down into Nadir is chained fast for Gala week.)"
                ),
            }],
        })
    # (4) East/NE Spur: 602 Candle Down
    for cy in (21, 22, 23, 24):
        E.append({
            'type': 'event',
            'name': 'To Candle Down',
            'at': [149, cy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    602, 2, 55, 'right',
                    "(The Crown Road east toward Candle Down is torn up for mending. 'Back in a month,' the sign says.)"
                ),
            }],
        })

    # CANON ROADBLOCK & AMBIENT NPCs (story/24_SCRIPT_CH5.md:213-282)
    E += [
        _npc((7, 22), 'Royal Forester', 'trainer_POKEMONRANGER_M', [
            "Royal Forester: The Verdance road. The Queen's road, by the Queen's leave.",
            "Royal Forester: Pass, or no passage.",
        ], d='right'),
        _npc((44, 7), 'Tithe-reeve', 'trainer_GENTLEMAN', [
            "Tithe-reeve: Kingsmead's the Accord's paddocks. Nobody past the reeve without a seal.",
            "Tithe-reeve: I'm the reeve.",
        ], d='down'),
        _npc((120, 70), 'Lift Guard', 'trainer_ENGINEER', [
            "Lift Guard: The Long Drop. Down to Nadir.",
            "Lift Guard: Nobody's going down this week. Gala week.",
            "Lift Guard: ...You don't want Nadir anyway. Nadir comes up to you.",
        ], d='up'),
        _npc((143, 23), 'Road-mender', 'NPC 14', [
            "Road-mender: Crown Road east is up for mending. Back in a month.",
            "Road-mender: It's been back in a month since spring.",
        ], d='left'),
        _npc((54, 34), 'Tithe-collector', 'NPC 25', [
            "Tithe-collector: A tithe for the Accord, a tithe for the Queen. They both take a tenth.",
            "Tithe-collector: Farmers here keep eight. They used to keep nine. Ask me how I sleep.",
        ], d='down'),
        _npc((72, 50), 'Barley Farmer', 'NPC 14', [
            "Barley Farmer: Half the sun, all the tithe.",
            "Barley Farmer: My barley's the best in Elowen because it's had to try.",
        ], d='down'),
        _npc((14, 39), 'Four Ways Innkeeper', 'NPC 18', [
            "Innkeeper: Welcome to The Four Ways! Warm pie, cold cider, and a mounting block that sees half Velmora pass by.",
            "Innkeeper: Don't ask me who nailed that blank fifth arm onto the signpost pointing at the Crownwall. Nobody admits to it.",
        ], d='down'),
        _npc((109, 57), 'Shrine-keeper', 'NPC 25', [
            "Shrine-keeper: \"And keep the One.\" Every prayer ends that way.",
            "Shrine-keeper: I've said it forty years. The Choir says it means the Sovereign.",
            "Shrine-keeper: My gran said it meant the Ogre. Nobody's ever told me to my face.",
        ], d='up'),
    ]

    # ALL 5 CONFIRMED PBS TRAINERS FROM pbs/trainers.txt (# Map 594 Wallshadow Row!)
    E += [
        _trainer((64, 32), 'AROMALADY', 'Linnet',
                 "Linnet: The meadow herbs grow sharpest here in the Crownwall's shadow—let's see if your team thrives in the shade!",
                 "Linnet: They do better in the Wall's shade. So do I, usually.",
                 d='down', sight=4),
        _trainer((51, 46), 'YOUNGSTER', 'Hodge',
                 "Hodge: Hey! You crossed the barley hedgerow without paying toll! Battle me instead!",
                 "Hodge: I'm telling the tithe-reeve. He won't care either.",
                 d='up', sight=4),
        _trainer((31, 46), 'LASS', 'Marigold',
                 "Marigold: Four kingdoms meet at The Four Ways—and I've challenged trainers from all of them! Your turn!",
                 "Marigold: Four kingdoms on that signpost and I lost in this one.",
                 d='up', sight=4),
        _trainer((88, 37), 'TAMER', 'Hob',
                 "Hob: Mind the Accord's tithe wagons! My hounds keep the road clear—show me your footing!",
                 "Hob: Tithe barn's full. My pride isn't.",
                 d='down', sight=4),
        _trainer((129, 44), 'TWINS', 'Meg & Peg',
                 "Meg & Peg: Two roads! Two barns! Two of us! Ready for a Crown Road double battle?",
                 "Meg: Your fault. Peg: YOUR fault.",
                 d='up', sight=4, rules=['setBattleRule("double")']),
    ]

    # CANON SIGNS, MILESTONES, SHRINE INSPECTS, SECRET CAVE & 4 THEMATIC ITEM PICKUPS
    E += [
        _sign((142, 37), 'Wallshadow Road Sign',
              "WALLSHADOW ROW — The Crown Road. ← Coppice Ride · ↓ the Arc-Lamp Mile & Lumen · → Candle Down · ↑ Kingsmead. Mind the tithe-reeve."),
        _sign((45, 42), 'Milestone XVII',
              "MILESTONE XVII: \"THE CROWN ROAD — XVII. Southgate 1.\""),
        _sign((108, 41), 'Milestone XVIII',
              "MILESTONE XVIII: \"XVIII. SOUTHGATE. Crownhaven: no road.\""),
        _sign((26, 45), 'Four-Kingdom Signpost',
              "FOUR-KINGDOM SIGNPOST: ← ISENMAR (THE LOCKS) · ↑ ELOWEN (VERDANCE, BY PRISM FALLS) · ↓ ZENITH (LUMEN) · ↘ NADIR (THE LONG DROP). A fifth arm has been nailed on, pointing straight at the Crownwall. It's blank."),
        _sign((107, 56), 'Prayer Board',
              "PRAYER BOARD: \"...that the Eighteen keep their peace, and the land its shape, and the Sovereign his strength; and keep the One.\""),
        _sign((111, 55), 'Southgate Chapel Window',
              "SOUTHGATE CHAPEL WINDOW: Eighteen panes of coloured glass around one clear pane. The clear pane in the middle catches the sun and throws it on the floor as a small colourless star."),
        _sign((108, 55), 'Southgate Shrine Door',
              "SOUTHGATE SHRINE — A small stone chapel where the Crown Road meets the road down to Lumen. Inside, cool stone smells of beeswax and rain."),
        _sign((53, 32), 'West Tithe Barn Door',
              "ACCORD TITHE BARN IV — Carved over the lintel: eighteen rings around one blank circle. Stacked sacks of Wallshadow barley fill the eaves."),
        _sign((86, 33), 'East Tithe Barn Door',
              "ACCORD TITHE BARN V — Chalk tallies mark every tenth sheaf collected for the Accord, and every tenth for the Queen."),
        _sign((13, 38), 'Four Ways Inn Door',
              "THE FOUR WAYS INN — Hot pies, Elowen cider, and dry stabling. The innkeeper insists the mounting block outside is luckier than any signpost."),
        _sign((74, 16), 'Bricked-Up Accord Cave',
              "A narrow cave mouth cut into the Crownwall's white chalk foot, bricked up with old Accord mortar. Several bricks are loose—cold air seeps out, smelling of wet chalk and faraway bells."),
        _item((22, 65), 'SUPERPOTION', 'Four Ways Glade Super Potion'),
        _item((76, 70), 'GREATBALL', 'Brook Meadow Great Ball'),
        _item((117, 19), 'MIRACLESEED', 'Wallshadow Knoll Miracle Seed'),
        _item((76, 18), 'REVIVE', 'Accord Cave Loose-Brick Revive', hidden=True),
    ]

    m.keep_clear |= {
        (148, 40), (147, 40), (149, 38), (149, 39), (149, 40), (149, 41), (149, 42),
        (148, 38), (148, 39), (148, 41), (148, 42),
        (0, 40), (0, 41), (0, 42), (1, 41),
        (0, 22), (0, 23), (43, 1), (44, 1), (44, 2), (44, 3), (44, 4), (44, 5), (44, 6), (44, 7),
        (122, 70), (122, 71), (149, 22), (149, 23),
        (74, 16), (74, 17), (73, 17), (75, 17), (74, 18), (75, 18), (76, 18),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))

    m.forest = lambda *a, **kw: _paint_woods_custom(m, CK.ELOWEN, seed=5941)

    # ---- 10. Paint Full Map + Post-Paint High-Craft Details ----
    m.paint()

    # Graceful Slender Warm-Timber Plank Footbridge anchored solidly to mainland grass banks (x=63..67, y=59..60)!
    nf0, nf1 = P1('N_f0'), P1('N_f1')
    for x in range(63, 68):
        m.L[0, 59, x] = nf0 if x % 2 == 0 else nf1
        m.L[0, 60, x] = nf1 if x % 2 == 0 else nf0
        m.L[1, 59, x] = 0
        m.L[1, 60, x] = 0
        if m.cls[58, x] in ('w', 'W'):
            m.L[1, 58, x] = P1('lm_railing_w' if x == 63 else 'lm_railing_e' if x == 67 else 'lm_railing_m')
        if m.cls[61, x] in ('w', 'W'):
            m.L[1, 61, x] = P1('lm_railing_w' if x == 63 else 'lm_railing_e' if x == 67 else 'lm_railing_m')
    # Solid shoreline bridge-end abutment bollards planted firmly on mainland grass (62/68, 58/61)!
    for bx, by in ((62, 58), (62, 61), (68, 58), (68, 61)):
        if m.cls[by, bx] == '.' and not m.taken[by, bx]:
            m.L[1, by, bx] = P1('lm_bollard')

    # Riveted-steel lift platform grate at The Long Drop (121..123, 71)
    for gx in (121, 122, 123):
        m.L[0, 71, gx] = P1('Q_f0' if gx % 2 == 0 else 'Q_f1')
        m.L[1, 71, gx] = P1('lm_grate')

    # Coherent Organic Elowen Wildflower Drifts, Clover Meadows & Woodland/Cliff Edge Undergrowth!
    rng = random.Random(59499)
    ts60 = R.tilesets()[TID]
    flower_tiles = [t for t in K.DECOR_SH['flowers'] if ts60['passages'][t] == 0]
    green_pass = [t for t in K.DECOR_SH['green'] if ts60['passages'][t] == 0]
    tuft_tiles = [P1('gr_tuft%d' % i) for i in range(3)] + [P1('gr_clover0'), P1('gr_clover1')] + green_pass
    ferns_pass = [P1('nt_fern0'), P1('nt_fern1')]

    flower_clumps = [
        (16, 45, 4, 2), (28, 37, 3, 2), (37, 45, 4, 2), (48, 35, 3, 2), (61, 35, 4, 2),
        (76, 35, 3, 2), (91, 38, 4, 2), (102, 51, 3, 2), (115, 53, 3, 2), (128, 37, 4, 2),
        (138, 46, 4, 2), (56, 52, 3, 2), (73, 53, 3, 2), (106, 20, 4, 2), (18, 21, 3, 2),
        (33, 56, 4, 2), (87, 56, 3, 2), (32, 35, 3, 2), (118, 30, 4, 2),
        # Expanded organic drifts across SW meadow, Southgate gardens, pond banks, and NE terraces
        (13, 62, 5, 3), (22, 55, 4, 3), (26, 63, 4, 3), (45, 56, 4, 3), (52, 65, 5, 3),
        (63, 43, 5, 2), (72, 62, 4, 3), (82, 46, 4, 3), (102, 62, 5, 3), (110, 62, 4, 3),
        (120, 56, 4, 3), (129, 64, 4, 3), (102, 34, 4, 3), (133, 23, 4, 2), (136, 35, 4, 2),
    ]
    for fx0, fy0, fw, fh in flower_clumps:
        for dy in range(fh):
            for dx in range(fw):
                fx, fy = fx0 + dx, fy0 + dy
                if m.inb(fx, fy) and m.cls[fy, fx] == '.' and not m.taken[fy, fx] and not m.cliff[fy, fx] and m.L[1, fy, fx] == 0 and m.L[2, fy, fx] == 0:
                    if (fx, fy) not in m.keep_clear and rng.random() < 0.78:
                        m.L[1, fy, fx] = rng.choice(flower_tiles)

    # Rich edge undergrowth hugging woods, cliffs, fences, buildings & water banks + soft rolling clover/tuft meadow drifts
    t_edge = np.zeros((H, W), bool)
    hard = (m.cls == 'T') | (m.cls == 'B') | m.cliff | np.isin(m.cls, ['w', 'W'])
    t_edge[1:, :] |= hard[:-1, :]
    t_edge[:-1, :] |= hard[1:, :]
    t_edge[:, 1:] |= hard[:, :-1]
    t_edge[:, :-1] |= hard[:, 1:]
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.' or m.taken[y, x] or m.cliff[y, x] or m.L[1, y, x] != 0 or m.L[2, y, x] != 0:
                continue
            if (x, y) in m.keep_clear:
                continue
            nz_fl = vnoise(x, y, 59501, 5.5)
            nz_cl = vnoise(x, y, 59502, 4.2)
            if t_edge[y, x]:
                if rng.random() < 0.62:
                    m.L[1, y, x] = rng.choice(ferns_pass if rng.random() < 0.30 else tuft_tiles)
            elif nz_fl > 0.62 and rng.random() < 0.78:
                m.L[1, y, x] = rng.choice(flower_tiles)
            elif nz_cl > 0.44 and rng.random() < 0.68:
                m.L[1, y, x] = rng.choice(tuft_tiles)

    # FINAL AUTOTILE PASS (after ALL post-paint overrides -> guarantees EXACTLY 0 NB2AUTO mismatches!)
    _fix_all_autotiles(m)

    # ---- 11. Full Essentials Directional BFS Verification from Arrival (148, 40)! ----
    _bfs_check(m, (148, 40), [
        ('East Warp to 593 Arc-Lamp Mile', (149, 40), False),
        ('West Exit to 595 Coppice Ride', (0, 41), False),
        ('NW Exit to 681 Prism Falls', (0, 23), False),
        ('North Exit to 756 Kingsmead', (43, 1), False),
        ('SE Long Drop Lift (672)', (122, 71), False),
        ('NE Spur to 602 Candle Down', (149, 23), False),
        ('Four Ways Inn & Signpost', (26, 45), True),
        ('Milestone XVII', (45, 42), True),
        ('Milestone XVIII', (108, 41), True),
        ('Southgate Shrine & Window', (111, 55), True),
        ('Secret Bricked-Up Cave', (74, 16), True),
        ('Hidden Cave Revive', (76, 18), True),
        ('Trainer: Aroma Lady Linnet', (64, 32), True),
        ('Trainer: Youngster Hodge', (51, 46), True),
        ('Trainer: Lass Marigold', (31, 46), True),
        ('Trainer: Tamer Hob', (88, 37), True),
        ('Trainer: Twins Meg & Peg', (129, 44), True),
        ('Item: Super Potion', (22, 65), True),
        ('Item: Great Ball', (76, 70), True),
        ('Item: Miracle Seed', (117, 19), True),
    ] + [(e.get('name', 'ev'), tuple(e['at']), True) for e in E if e and e.get('at')], 'Map 594')

    head = {
        'id': 594,
        'name': 'Wallshadow Row',
        'parent': 0,
        'bgm': 'Route 2',
        'field': 'MEADOW',
        'map_audio': {'bgm': 'Route - Elowen', 'bgs': '', 'rain': True},
        'metadata': {'Name': 'Wallshadow Row', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 11, 9]},
        'tone': [0, 2, -2, 0],
        '_file': '594_wallshadow_row.yaml',
    }
    m.write(594, head, comment='# GENERATED by mapgen/layouts/wallshadow_row.py (Ch5): Wallshadow Row (story/24_SCRIPT_CH5.md).\n'
                               '# Edit the layout script, not this file.\n')
    return m


def main():
    build_594()
    print('Done: wrote specs/594_wallshadow_row.yaml and raw 594.npy.')


if __name__ == '__main__':
    main()
