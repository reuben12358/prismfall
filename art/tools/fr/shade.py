"""Rim/edge shading on hand-drawn character grids (char level).
ramps: list of [dark, mid, light, highlight] char ramps; every pixel of a
ramp is re-toned by its distance to the outline on the lit (upper-left)
side vs the shadow (lower-right) side."""


def rim(rows, ramps, light=(-1, -1), keep=(), keep_interior=()):
    g = [list(r) for r in rows]
    h, w = len(g), len(g[0])
    lut = {}
    for rp in ramps:
        for ch in rp:
            lut[ch] = rp
    edge = lambda y, x: not (0 <= y < h and 0 <= x < w) or g0[y][x] in '.0'
    g0 = [r[:] for r in g]
    for y in range(h):
        for x in range(w):
            ch = g0[y][x]
            if ch not in lut or ch in keep:
                continue
            rp = lut[ch]
            lu1 = edge(y - 1, x) or edge(y, x - 1)
            lu2 = edge(y - 2, x) or edge(y, x - 2) or edge(y - 1, x - 1)
            dr1 = edge(y + 1, x) or edge(y, x + 1)
            dr2 = edge(y + 2, x) or edge(y, x + 2) or edge(y + 1, x + 1)
            if lu1 and not dr1:
                g[y][x] = rp[3]
            elif lu2 and not dr1:
                g[y][x] = rp[2]
            elif dr1:
                g[y][x] = rp[0]
            elif dr2:
                g[y][x] = rp[0] if ch == rp[0] else rp[1]
            else:
                if ch in keep_interior:
                    continue
                g[y][x] = rp[1] if ch not in (rp[0],) else rp[0]
    return [''.join(r) for r in g]


def notch(rows, pts):
    """Cut transparent wedges (lists of (x, y)) and outline their borders."""
    g = [list(r) for r in rows]
    for x, y in pts:
        g[y][x] = '.'
    h, w = len(g), len(g[0])
    for x, y in pts:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            X, Y = x + dx, y + dy
            if 0 <= X < w and 0 <= Y < h and g[Y][X] not in '.0':
                g[Y][X] = '0'
    return [''.join(r) for r in g]
