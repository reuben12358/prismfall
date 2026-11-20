"""passguard: decorations must never make a solid tile walkable (map builder 11, the passability audit).

Essentials' playerPassable? reads a cell's layers top-down and stops at the first tile with priority 0 that has no
blocked passage bits: that tile decides, and everything under it is ignored. So a passable decal on the top layer
(a crack, a shell, a fern, a silk thread) over a solid prop, cliff or water makes that prop walkable in the game,
although every preview shows it solid.

A DECORATION is a sheet tile (id >= 384) with priority 0, no passage bits and no bridge / neutral tag that is not a
walking surface. Walking surfaces (stairs, bridges, planks, decks, wet sand, mats, autotiles...) are meant to be
walked on over whatever is under them. Named tiles (rkit STAMPS / ndraw / tdraw pieces, hallkit CU names) are
judged by name (WALK below); unnamed sheet tiles by coverage (an opaque tile is a floor, a sparse one a decal).

A HIT is a cell, without an event, that Essentials lets the player onto only because of a decoration, and that the
player can actually reach (4-neighbour flood from cells that are walkable without decorations, or from surfable
water). `hits()` is the check build.py runs (PASS warnings, --strict fails); `guard()` is the fix every layout
writer applies before it saves its layers (rkit.Map.write, hallkit.Hall.write): it lifts the decoration off the hit
cells, so the solid tile under it rules again.
"""
import os
import re
import sys
from collections import deque

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WALK = re.compile(r'stair|bridge|plank|pier|boardwalk|_wet|wet_|deck|jetty|step|ramp|floor|rug|mat_|_mat|carpet|'
                  r'path|road|quay|wharf|causeway|slab|ladder|walk|door|gate|arch|tread|landing|terrace|crossing|'
                  r'ford|duckboard|ice|snow|sand|mud|dirt|gravel|cobble|pave|tile|board|trench|rut|'
                  r'^bw_|^sb_|^fw_log', re.I)
# unnamed sheet tiles that are walking surfaces whatever their coverage: tileset 54's door-notch frame pieces either
# side of an exit mat (the notch is three cells wide and all of it is floor)
SURFACE_IDS = {54: {686, 687, 912, 914, 1795, 1797}}
NEUTRAL_TAGS = (13, 15)          # Neutral (ignore passability) and Bridge (ignored off-bridge)
SURF_TAGS = (5, 6, 7)            # DeepWater, StillWater, Water
_CACHE = {}


def _names():
    if 'names' in _CACHE: return _CACHE['names']
    names = {}
    sys.path.insert(0, os.path.join(HERE, 'layouts'))
    try:
        import rkit as K
        for n, st in K.STAMPS.items():
            for L in st['layers']:
                for row in L:
                    for t in row:
                        if t: names.setdefault(('pf', t), n)
    except Exception:
        pass
    try:
        import hallkit as H
        for n, t in H._H['cu'].items(): names.setdefault((54, t), n)
    except Exception:
        pass
    _CACHE['names'] = names
    return names


def _coverage(ts, t):
    key = ('cov', ts['id'])
    if key not in _CACHE:
        import render as R
        from PIL import Image
        p = R.gfx('Tilesets', ts['tileset_name']) if ts.get('tileset_name') else None
        _CACHE[key] = np.array(Image.open(p).convert('RGBA'))[:, :, 3] if p else None
    a = _CACHE[key]
    if a is None: return 1.0
    i = t - 384; x, y = (i % 8) * 32, (i // 8) * 32
    c = a[y:y + 32, x:x + 32]
    return float((c > 0).mean()) if c.size else 1.0


def tile_name(tid, t):
    n = _names()
    return n.get((54, t)) if tid == 54 else n.get(('pf', t))


def decoration_table(ts):
    """bool array: tile id -> is a decoration (see module doc)."""
    key = ('deco', ts['id'])
    if key in _CACHE: return _CACHE[key]
    pas, pri, tag = ts['passages'], ts['priorities'], ts['terrain_tags']
    n = len(pas)
    out = np.zeros(n, dtype=bool)
    for t in range(384, n):
        if pas[t] & 0x0f or pri[t] != 0: continue
        if t < len(tag) and tag[t] in NEUTRAL_TAGS: continue
        nm = tile_name(ts['id'], t)
        if t in SURFACE_IDS.get(ts['id'], ()):
            continue
        if nm is not None:
            out[t] = not WALK.search(nm)
        else:
            out[t] = _coverage(ts, t) < 0.9
    _CACHE[key] = out
    return out


def _verdict(layers, ts, deco=None):
    """Essentials' playerPassable? for whole tiles (no events, not surfing, off-bridge); with `deco`, decorations
    are looked through. Vectorised: returns an H x W bool array."""
    pas = np.asarray(ts['passages']); pri = np.asarray(ts['priorities']); tag = np.asarray(ts['terrain_tags'])
    Z, H, W = layers.shape
    res = np.ones((H, W), dtype=bool); done = np.zeros((H, W), dtype=bool)
    for z in (2, 1, 0):
        t = layers[z]
        t = np.where(t < len(pas), t, 0)
        skip = (t == 0) | np.isin(tag[t], NEUTRAL_TAGS)
        if deco is not None: skip |= deco[t]
        live = ~done & ~skip
        solid = live & ((pas[t] & 0x0f) == 0x0f)
        res[solid] = False; done |= solid
        stop = live & ~solid & (pri[t] == 0)
        done |= stop
    return res


def hits(layers, ts, event_cells=()):
    """[(x, y, z, tile)]: the decoration tile that makes each reachable solid cell walkable."""
    layers = np.asarray(layers)
    deco = decoration_table(ts)
    actual = _verdict(layers, ts)
    intended = _verdict(layers, ts, deco)
    masked = actual & ~intended
    for x, y in event_cells:
        if 0 <= y < masked.shape[0] and 0 <= x < masked.shape[1]: masked[y, x] = False
    if not masked.any(): return []
    H, W = masked.shape
    seen = np.zeros_like(masked)
    q = deque()
    for y, x in np.argwhere(masked):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and intended[ny, nx] and not masked[ny, nx]:
                seen[y, x] = True; q.append((x, y)); break
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and masked[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((nx, ny))
    out = []
    for y, x in np.argwhere(seen):
        for z in (2, 1):
            t = int(layers[z, y, x])
            if t and t < len(deco) and deco[t]:
                out.append((int(x), int(y), z, t)); break
    return out


def blocker(ts):
    """an invisible solid tile of the sheet (fully transparent, all passage bits, priority 0, no terrain tag)"""
    key = ('block', ts['id'])
    if key not in _CACHE:
        pas, pri, tag = ts['passages'], ts['priorities'], ts['terrain_tags']
        _CACHE[key] = next((t for t in range(384, len(pas)) if pas[t] & 0x0f == 0x0f and pri[t] == 0 and
                            (t >= len(tag) or tag[t] == 0) and _coverage(ts, t) == 0.0), None)
    return _CACHE[key]


def guard(layers, tileset_id, event_cells=(), label=''):
    """The fix, in place, keeping the picture: on every hit cell the decoration moves down a layer (when there is
    room) and an invisible solid tile goes on top, so the cell draws as before and the solid tile under it rules again.
    With no room (a decal over a see-through solid prop on the ground layer) the decoration is lifted off."""
    import render as R
    ts = R.tilesets()[tileset_id]
    blk = blocker(ts)
    pri = ts['priorities']
    deco = decoration_table(ts)
    n = 0
    for _ in range(4):
        hs = hits(layers, ts, event_cells)
        if not hs: break
        for x, y, z, t in hs:
            n += 1
            l1, l0 = int(layers[1, y, x]), int(layers[0, y, x])
            if blk is None:
                layers[z, y, x] = 0
            elif z == 1 and not layers[2, y, x]:
                layers[2, y, x] = blk                              # decoration stays where it is, a lid on top
            elif z == 2 and l1 == 0:
                layers[1, y, x] = t; layers[2, y, x] = blk         # decoration down to layer 1
            elif z == 2 and pri[l1] == 0 and not deco[l1] and _coverage(ts, l1) >= 0.99:
                layers[0, y, x] = l1; layers[1, y, x] = t; layers[2, y, x] = blk   # an opaque prop hides the ground anyway
            else:
                layers[z, y, x] = 0                                # no room: lift the decoration
    if n and label: print('%s: passguard fixed %d decorated solid cell(s)' % (label, n))
    return n
