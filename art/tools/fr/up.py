"""Scale2x (EPX) + outline thinning: turns 48-px-native pixel art into
clean 96-px-native art with 1-px outlines that can then be hand-detailed."""
import numpy as np


def scale2x(a):
    h, w = a.shape[:2]
    P = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    E = P[1:-1, 1:-1]; B = P[:-2, 1:-1]; H = P[2:, 1:-1]; D = P[1:-1, :-2]; F = P[1:-1, 2:]
    eq = lambda x, y: (x == y).all(-1)
    out = np.zeros((h * 2, w * 2, 4), a.dtype)
    c1 = eq(D, B) & ~eq(D, H) & ~eq(B, F)
    c2 = eq(B, F) & ~eq(B, D) & ~eq(F, H)
    c3 = eq(D, H) & ~eq(D, B) & ~eq(H, F)
    c4 = eq(H, F) & ~eq(D, H) & ~eq(B, F)
    out[0::2, 0::2] = np.where(c1[..., None], D, E)
    out[0::2, 1::2] = np.where(c2[..., None], F, E)
    out[1::2, 0::2] = np.where(c3[..., None], D, E)
    out[1::2, 1::2] = np.where(c4[..., None], F, E)
    return out


def thin_outline(a, dark_max=60):
    """Where the dark outline is 2 px thick, recolour the inner pixel with
    the neighbouring interior colour (keeps silhouettes, halves line weight)."""
    out = a.copy()
    lum = a[..., :3].astype(int).sum(-1)
    dark = (lum <= dark_max * 3) & (a[..., 3] > 0)
    h, w = dark.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if not dark[y, x]:
                continue
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                # outer side: transparent or another region beyond a dark pair
                oy, ox = y - dy, x - dx       # neighbour on the opposite side
                ny, nx = y + dy, x + dx
                if dark[oy, ox] and 0 <= ny < h and 0 <= nx < w and not dark[ny, nx] and a[ny, nx, 3] > 0:
                    yy, xx = oy - dy, ox - dx
                    if 0 <= yy < h and 0 <= xx < w and (a[yy, xx, 3] == 0 or not dark[yy, xx]):
                        out[y, x] = a[ny, nx]
                        break
    return out
