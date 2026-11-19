#!/usr/bin/env python3
"""tdraw.py - city pieces for the PF Rejuv `pf` part (map builder 8): Saltmere's townhouses, warehouses and civic fronts,
stone and timber stairs, the masonry quay kit, harbour cranes, salt heaps, poster columns, the fountain, and grass
variation tiles.

Townhouses are KITBASHED from real Rejuvenation pixel art: roof and wall textures, windows and doors are sampled from
the Aevium Past, Sheridan and Goldenleaf sheets (all 2x art, sampled losslessly at the 16-px logical grid), recoloured
along ramps (roof: terracotta / crimson / slate / umber / plank; wall: clapboard and plaster colours), and assembled
with code-drawn structure: eaves and ridge lines, gable fronts with bargeboards, lit and shaded roof slopes, dormers,
chimneys, under-eave shadow, corner quoins, shutters, flower boxes, shop fronts, awnings and bracket signs.
Light from the top left; outlines never black (rdraw conventions).  rcustom.py doubles every piece exactly 2x.

    python3 -I tdraw.py out.png        # contact sheet of every piece (research)"""
import os, sys, json, math, random, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import rdraw as D
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = D.OUT
CLEAR = (0, 0, 0, 0)
P = D.P

# ------------------------------------------------------------------ source tiles (composite ids, read from the games)
_SRC = {}


def _part_of(cid):
    cfg = json.load(open(os.path.join(HERE, 'data', 'rj_compose.json')))['parts']
    best = None
    for k, v in cfg.items():
        if v['offset'] <= cid < v['offset'] + v['tiles'] and k != 'pf': best = (k, v)
    return best


def tex(cid):
    """a composite-id tile at the 16-px logical scale (2x art sampled at even pixels: lossless)"""
    k, v = _part_of(cid)
    key = v['sheet']
    if key not in _SRC:
        import rref as RR
        _SRC[key] = Image.open(os.path.join(RR.GAMES[v['game']], 'Graphics', 'Tilesets', key + '.png')).convert('RGBA')
    i = cid - v['offset']
    t = _SRC[key].crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32))
    return t.resize((16, 16), Image.NEAREST)


def stack(rows):
    """a block of composite tiles (rows of ids, 0 = empty) as one logical image"""
    h = len(rows); w = max(len(r) for r in rows)
    im = Image.new('RGBA', (w * 16, h * 16), CLEAR)
    for y, r in enumerate(rows):
        for x, t in enumerate(r):
            if t: im.alpha_composite(tex(t), (x * 16, y * 16))
    return im


def colours(im):
    return {px[:3] for px in im.getdata() if px[3]}


def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def ramp_map(im, ramp, select=None, keep=()):
    """recolour: every selected colour goes to the target ramp by its luminance rank (dark -> ramp[0])"""
    cs = sorted((c for c in colours(im) if (select is None or select(c)) and c not in keep), key=lum)
    if not cs: return im
    lo, hi = lum(cs[0]), lum(cs[-1])
    m = {}
    for c in cs:
        f = 0.0 if hi == lo else (lum(c) - lo) / (hi - lo)
        f = f * (len(ramp) - 1); i = min(len(ramp) - 2, int(f)); t = f - i
        a, b = ramp[i], ramp[i + 1]
        m[c] = tuple(int(round(a[j] + (b[j] - a[j]) * t)) for j in range(3))
    out = im.copy(); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            p = px[x, y]
            if p[3] and p[:3] in m: px[x, y] = m[p[:3]] + (p[3],)
    return out


def shade(c, f):
    return tuple(max(0, min(255, int(round(v * f)))) for v in c[:3]) + ((c[3],) if len(c) > 3 else (255,))


def tile_fill(dst, src, box, ox=0, oy=0):
    """fill box (x0, y0, x1, y1 exclusive) of dst with src tiled from (ox, oy)"""
    x0, y0, x1, y1 = box; sp = src.load(); dp = dst.load(); W, H = src.size
    for y in range(max(0, y0), min(dst.height, y1)):
        for x in range(max(0, x0), min(dst.width, x1)):
            p = sp[(x - ox) % W, (y - oy) % H]
            if p[3]: dp[x, y] = p


def key_out(im, keys, tol=0):
    out = im.copy(); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            p = px[x, y]
            if p[3] and (p[:3] in keys or (tol and any(abs(p[0] - k[0]) + abs(p[1] - k[1]) + abs(p[2] - k[2]) <= tol for k in keys))):
                px[x, y] = CLEAR
    return out


def crop_alpha(im):
    bb = im.getbbox(); return im.crop(bb) if bb else im


# ------------------------------------------------------------------ palettes (dark -> light)
RAMPS = {
    'terra':   [(92, 38, 30), (148, 62, 44), (196, 98, 70), (226, 140, 104), (246, 186, 150)],
    'crimson': [(70, 22, 32), (118, 34, 42), (160, 52, 54), (198, 84, 76), (228, 128, 110)],
    'slate':   [(40, 46, 62), (66, 76, 98), (96, 108, 132), (132, 146, 170), (170, 182, 204)],
    'umber':   [(56, 36, 30), (88, 58, 44), (120, 84, 62), (152, 114, 84), (186, 152, 118)],
    'moss':    [(40, 56, 46), (62, 84, 64), (88, 112, 82), (120, 142, 104), (160, 176, 132)],
    'teal':    [(30, 56, 66), (46, 84, 96), (66, 116, 126), (98, 150, 156), (142, 186, 186)],
}
WALLS = {   # plaster / clapboard ramps (shadow, body, light, highlight)
    'cream':  [(150, 136, 108), (206, 192, 160), (232, 222, 194), (246, 240, 220)],
    'ochre':  [(148, 108, 60), (204, 160, 92), (226, 190, 124), (240, 214, 160)],
    'rose':   [(150, 98, 98), (206, 146, 136), (226, 176, 164), (242, 206, 194)],
    'salmon': [(156, 92, 70), (214, 138, 106), (232, 168, 134), (246, 200, 170)],
    'sky':    [(96, 116, 140), (152, 178, 200), (186, 206, 222), (214, 228, 238)],
    'sage':   [(104, 122, 96), (160, 178, 142), (192, 206, 170), (218, 228, 198)],
    'white':  [(150, 150, 150), (214, 212, 204), (234, 232, 226), (248, 248, 244)],
    'lilac':  [(120, 104, 136), (176, 160, 190), (204, 192, 214), (226, 218, 232)],
}
STONE = [(78, 72, 74), (120, 112, 108), (156, 148, 138), (190, 182, 168), (216, 210, 196)]
SAND = [(110, 92, 70), (160, 140, 108), (196, 178, 142), (222, 208, 174), (238, 230, 204)]
BRICK = [(86, 36, 34), (136, 58, 46), (168, 82, 62), (196, 112, 84)]
WOOD = D.WOOD + [(176, 138, 98, 255)]
DKW = (56, 38, 34, 255)
GLASS = [(52, 70, 96, 255), (88, 122, 152, 255), (150, 184, 206, 255), (210, 230, 238, 255)]
LIT = [(196, 120, 60, 255), (255, 200, 104, 255), (255, 236, 168, 255)]
FLOWERS = [(226, 74, 86, 255), (244, 150, 170, 255), (250, 220, 110, 255), (180, 120, 220, 255), (250, 250, 250, 255)]
LEAF = [(40, 96, 56, 255), (66, 140, 72, 255), (110, 180, 96, 255)]

# ------------------------------------------------------------------ textures
_TEX = {}


def roof_tex(kind):
    if kind in _TEX: return _TEX[kind]
    if kind in ('terra', 'crimson', 'umber_t', 'slate_t'):
        t = tex(11682)                                                   # Aevium Past barrel tiles
        ramp = {'terra': None, 'crimson': RAMPS['crimson'], 'umber_t': RAMPS['umber'], 'slate_t': RAMPS['slate']}[kind]
        if ramp: t = ramp_map(t, ramp)
    elif kind in ('diamond', 'slate', 'moss', 'teal'):
        t = tex(13766)                                                   # Aevium Past diamond shingles
        if kind != 'diamond': t = ramp_map(t, RAMPS[kind])
    elif kind in ('plank', 'plank_b', 'shingle', 'shingle_m'):
        t = shingle_tex({'plank': 'slate', 'plank_b': 'umber', 'shingle': 'slate', 'shingle_m': 'moss'}[kind])
    else:
        raise KeyError(kind)
    _TEX[kind] = t
    return t


def shingle_tex(rk):
    """split slate / shingle courses (16x16, seamless): staggered 4-px slates with a lit top edge and a dark butt line"""
    r = RAMPS[rk]; im = Image.new('RGBA', (16, 16), r[2] + (255,)); d = ImageDraw.Draw(im); rng = random.Random(len(rk))
    for k in range(4):
        y = k * 4; off = 0 if k % 2 == 0 else 2
        for x in range(-off, 16, 4):
            c = r[2] if rng.random() < 0.6 else r[3] if rng.random() < 0.5 else r[1]
            d.rectangle([x, y, x + 3, y + 3], fill=c + (255,))
            d.line([x, y, x + 2, y], fill=r[min(4, r.index(c) + 1)] + (255,))
            d.line([x + 3, y, x + 3, y + 3], fill=r[0] + (255,))
        d.line([0, y + 3, 15, y + 3], fill=r[0] + (255,))
    return im


def plaster(col, w, h, seed):
    """flat plaster with a faint speckle and a few hairline cracks"""
    r = WALLS[col]; rng = random.Random(seed)
    im = Image.new('RGBA', (w, h), r[1] + (255,)); px = im.load()
    for _ in range(w * h // 14):
        x, y = rng.randrange(w), rng.randrange(h); px[x, y] = r[2] + (255,) if rng.random() < 0.55 else shade(r[1], 0.94)
    for x in range(w):                                    # soft light from the west, a little grime toward the base
        f = 1.04 - 0.08 * x / max(1, w - 1)
        for y in range(h):
            g = 0.93 if y >= h - 3 else 0.97 if y >= h - 6 else 1.0
            p = px[x, y]; px[x, y] = shade(p, f * g)
    return im


def clapboard(col, w, h):
    t = tex(13779)
    keys = sorted(colours(t), key=lum)
    t2 = ramp_map(t, WALLS[col]) if col != 'native' else t
    im = Image.new('RGBA', (w, h), CLEAR); tile_fill(im, t2.crop((0, 0, 8, 16)), (0, 0, w, h))
    return im


def ashlar(w, h, ramp=STONE, seed=1, course=5, block=(7, 11)):
    """dressed stone: courses `course` px tall, staggered blocks, light top edge, dark mortar"""
    rng = random.Random(seed)
    im = Image.new('RGBA', (w, h), ramp[2] + (255,)); d = ImageDraw.Draw(im)
    y = 0; k = 0
    while y < h:
        x = -rng.randrange(0, 6) if k % 2 else 0
        while x < w:
            bw = rng.randrange(*block)
            c = ramp[2] if rng.random() < 0.7 else ramp[3] if rng.random() < 0.5 else ramp[1]
            d.rectangle([x, y, x + bw - 1, y + course - 1], fill=c + (255,))
            d.line([x, y, x + bw - 2, y], fill=ramp[3 if c != ramp[3] else 4] + (255,))
            d.line([x + bw - 1, y, x + bw - 1, y + course - 1], fill=ramp[0] + (255,))
            x += bw
        d.line([0, y + course - 1, w, y + course - 1], fill=ramp[0] + (255,))
        y += course; k += 1
    return im


def brick(w, h, seed=2):
    rng = random.Random(seed)
    im = Image.new('RGBA', (w, h), BRICK[2] + (255,)); d = ImageDraw.Draw(im)
    for y in range(0, h, 3):
        d.line([0, y + 2, w, y + 2], fill=(150, 130, 120, 255))
        off = 0 if (y // 3) % 2 else 3
        for x in range(off, w, 6):
            d.line([x, y, x, y + 1], fill=(150, 130, 120, 255))
            if rng.random() < 0.3: d.line([x + 1, y, x + 4, y], fill=BRICK[3] + (255,))
            elif rng.random() < 0.2: d.line([x + 1, y + 1, x + 4, y + 1], fill=BRICK[1] + (255,))
    return im


def timber_band(w, h):
    """Sheridan half-timbering: real cross-braced panels (sh 5842/5843) tiled across"""
    t = stack([[5843]])
    im = Image.new('RGBA', (w, h), CLEAR); tile_fill(im, t, (0, 0, w, h))
    return im


# ------------------------------------------------------------------ window and door sprites (real tiles, wall keyed out)
_SPR = {}


def sprite(name):
    if name in _SPR: return _SPR[name]
    if name == 'arch':                       # Aevium Past arched sash window (clapboard keyed out)
        im = stack([[13777], [13785]]); keys = colours(stack([[13779], [13787]]))
        im = key_out(im, keys, tol=10)
    elif name == 'shlit':                    # Sheridan lit arched window (plaster keyed)
        im = stack([[5841], [5849]]).crop((0, 8, 16, 24)); keys = colours(stack([[5841]]).crop((0, 0, 16, 6)))
        im = key_out(im, keys, tol=12)
    elif name == 'shdia':                    # Sheridan diamond window
        im = stack([[5840], [5848]]).crop((0, 8, 16, 24)); keys = colours(stack([[5840]]).crop((0, 0, 16, 6)))
        im = key_out(im, keys, tol=12)
    elif name == 'mans':                     # Aevium Past white-framed sash (mansard front)
        im = stack([[11593]]); keys = {c for c in colours(stack([[11593]]).crop((0, 12, 16, 16)))}
        im = stack([[11593]]).crop((1, 0, 9, 11))
    elif name == 'shdoor':                   # Sheridan plank door in its timber frame
        im = stack([[5873], [5881]])
    elif name == 'apdoor':                   # Aevium Past panelled door in a moulded frame
        im = stack([[13779, 13780, 13781], [13787, 13788, 13789]]); keys = colours(stack([[13779], [13787]]).crop((0, 0, 8, 32)))
        im = crop_alpha(key_out(im, keys, tol=10))
    else:
        raise KeyError(name)
    im = crop_alpha(im)
    _SPR[name] = im
    return im


# ------------------------------------------------------------------ drawing helpers
def outline_rect(d, box, c=OUT):
    d.rectangle(box, outline=c)


def window(im, x, y, kind, wall, rng, shutters=None, box=False, lit=False):
    """a window at (x, y) top-left (logical px); kinds: arch / shlit / shdia (real sprites) or sash / tall / round (drawn)"""
    d = ImageDraw.Draw(im)
    if kind in ('arch', 'shlit', 'shdia'):
        s = sprite(kind); im.alpha_composite(s, (x, y)); w, h = s.size
    else:
        w, h = {'sash': (7, 10), 'tall': (7, 13), 'small': (6, 7), 'wide': (10, 8)}[kind]
        fr = WOOD[3] if rng.random() < 0.5 else (236, 232, 222, 255)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=fr, outline=DKW)
        g = LIT if lit else GLASS
        d.rectangle([x + 1, y + 1, x + w - 2, y + h - 2], fill=g[1])
        d.rectangle([x + 1, y + h // 2, x + w - 2, y + h - 2], fill=g[0] if not lit else g[1])
        d.line([x + 1, y + 1, x + 1, y + h - 2], fill=g[2]); P(im, x + 2, y + 1, g[3 if not lit else 2]); P(im, x + 2, y + 2, g[2])
        mx = x + w // 2; my = y + h // 2
        d.line([mx, y + 1, mx, y + h - 2], fill=fr); d.line([x + 1, my, x + w - 2, my], fill=fr)
        d.line([x, y + h, x + w - 1, y + h], fill=shade(wall[0], 1.0))           # sill shadow
        d.line([x - 1, y + h - 1, x + w, y + h - 1], fill=(220, 214, 204, 255))  # sill
    if shutters:
        sc = shutters
        for sx in (x - 3, x + w):
            d.rectangle([sx, y, sx + 2, y + h - 2], fill=sc[1], outline=shade(sc[0], 0.9))
            d.line([sx + 1, y + 1, sx + 1, y + h - 3], fill=sc[2])
    return w, h


def flowerbox(im, x, y, w, rng):
    d = ImageDraw.Draw(im)
    d.rectangle([x, y, x + w - 1, y + 2], fill=WOOD[2], outline=DKW)
    for i in range(x, x + w):
        if rng.random() < 0.8: P(im, i, y - 1, rng.choice(LEAF[1:]))
        if rng.random() < 0.5: P(im, i, y - 2 + rng.randrange(2), rng.choice(FLOWERS))


SHUT = [[(40, 70, 104, 255), (58, 104, 150, 255), (96, 146, 186, 255)], [(36, 78, 50, 255), (52, 116, 70, 255), (90, 160, 100, 255)],
        [(98, 34, 36, 255), (150, 52, 52, 255), (196, 92, 84, 255)], [(70, 54, 40, 255), (110, 82, 56, 255), (150, 116, 80, 255)]]
AWN = [[(150, 40, 44), (236, 228, 214)], [(40, 92, 140), (236, 228, 214)], [(44, 112, 70), (238, 222, 170)],
       [(196, 140, 40), (244, 236, 210)], [(110, 52, 110), (236, 228, 214)]]


def awning(im, x0, x1, y, cols, depth=5):
    """a striped canvas awning over a shop front, scalloped hem, shadow below"""
    d = ImageDraw.Draw(im); a, b = cols
    for x in range(x0, x1 + 1):
        c = a if ((x - x0) // 3) % 2 == 0 else b
        d.line([x, y, x, y + depth - 1], fill=c + (255,))
        P(im, x, y, shade(c + (255,), 1.15))
    for x in range(x0, x1 + 1, 3):
        d.polygon([(x, y + depth), (x + 1, y + depth + 1), (x + 2, y + depth)], fill=(a if ((x - x0) // 3) % 2 == 0 else b) + (255,))
    d.line([x0, y, x1, y], fill=OUT); d.line([x0 - 1, y, x0 - 1, y + depth - 1], fill=OUT); d.line([x1 + 1, y, x1 + 1, y + depth - 1], fill=OUT)
    d.line([x0, y + depth + 2, x1, y + depth + 2], fill=(0, 0, 0, 60))


def bracket_sign(im, x, y, col, emblem, rng):
    """an iron bracket with a painted board hanging from it"""
    d = ImageDraw.Draw(im)
    d.line([x, y, x + 6, y], fill=D.IRON[1]); d.line([x, y + 1, x + 2, y], fill=D.IRON[0]); P(im, x + 6, y + 1, D.IRON[1])
    d.rectangle([x + 2, y + 2, x + 8, y + 8], fill=col[1], outline=OUT)
    d.line([x + 3, y + 3, x + 7, y + 3], fill=col[2])
    ex, ey = x + 5, y + 6
    if emblem == 'fish': d.line([ex - 2, ey, ex + 1, ey], fill=(230, 230, 236, 255)); P(im, ex + 2, ey - 1, (230, 230, 236, 255)); P(im, ex + 2, ey + 1, (230, 230, 236, 255))
    elif emblem == 'mug': d.rectangle([ex - 2, ey - 2, ex, ey + 1], fill=D.GOLD[1]); P(im, ex + 1, ey - 1, D.GOLD[1])
    elif emblem == 'key': d.line([ex - 2, ey, ex + 1, ey], fill=D.GOLD[2]); P(im, ex - 2, ey - 1, D.GOLD[2]); P(im, ex + 1, ey + 1, D.GOLD[2])
    elif emblem == 'mask': d.ellipse([ex - 2, ey - 2, ex + 1, ey + 1], fill=D.GOLD[2]); P(im, ex - 1, ey - 1, OUT); P(im, ex, ey - 1, OUT)
    else: d.ellipse([ex - 2, ey - 2, ex + 1, ey + 1], fill=D.GOLD[1])


def chimney(im, x, y, h=7, ramp=STONE):
    d = ImageDraw.Draw(im)
    d.rectangle([x, y, x + 4, y + h], fill=ramp[2] + (255,), outline=OUT)
    d.line([x + 1, y + 1, x + 1, y + h - 1], fill=ramp[3] + (255,)); d.line([x + 3, y + 1, x + 3, y + h - 1], fill=ramp[1] + (255,))
    d.rectangle([x - 1, y - 1, x + 5, y + 1], fill=ramp[3] + (255,), outline=OUT)
    d.rectangle([x + 1, y - 1, x + 3, y], fill=(60, 50, 50, 255))


def shade_box(im, box, f):
    x0, y0, x1, y1 = box; px = im.load()
    for y in range(max(0, y0), min(im.height, y1)):
        for x in range(max(0, x0), min(im.width, x1)):
            p = px[x, y]
            if p[3]: px[x, y] = shade(p, f)


# ------------------------------------------------------------------ the townhouse
def townhouse(W, roof_rows, floors, roof='terra', wall=('plaster', 'cream'), door=1, gable=False, seed=1, shop=None,
              wins='sash', ground=None, dormers=0, chim=(), shutters=None, boxes=0.0, sign=None, quoin=True, lit=False,
              cross=False, hoist=False, bigdoor=False):
    """W tiles wide.  roof_rows: roof height in tiles; floors: list of upper-storey heights in px (the ground floor is
    always the bottom 24 px: a door row).  Returns (image, code rows, door cell)."""
    rng = random.Random(seed)
    wall_h = sum(floors) + 24
    H = roof_rows + -(-wall_h // 16)
    w, h = W * 16, H * 16
    im = Image.new('RGBA', (w, h), CLEAR); d = ImageDraw.Draw(im)
    fy = h - wall_h                     # facade top (eave line)
    # ---------------- facade
    kind = wall[0]; col = wall[1] if len(wall) > 1 else 'cream'
    if kind == 'plaster': fac = plaster(col, w, wall_h, seed)
    elif kind == 'clap': fac = clapboard(col, w, wall_h)
    elif kind == 'stone': fac = ashlar(w, wall_h, STONE if col != 'sand' else SAND, seed)
    elif kind == 'brick': fac = brick(w, wall_h, seed)
    elif kind == 'timber': fac = plaster('cream', w, wall_h, seed)
    else: raise KeyError(kind)
    im.alpha_composite(fac, (0, fy))
    wr = WALLS.get(col, WALLS['cream']) if kind in ('plaster', 'clap', 'timber') else [STONE[1], STONE[2], STONE[3], STONE[4]]
    # ground floor material (stone plinth storey for shops / warehouses)
    gtop = h - 24
    if ground == 'stone':
        im.alpha_composite(ashlar(w, 24, STONE, seed + 7), (0, gtop))
    elif ground == 'sand':
        im.alpha_composite(ashlar(w, 24, SAND, seed + 7), (0, gtop))
    elif ground == 'timber':
        g = Image.new('RGBA', (w, 24), WOOD[2]); gd = ImageDraw.Draw(g)
        for x in range(0, w, 4): gd.line([x, 0, x, 23], fill=WOOD[1]); gd.line([x + 1, 0, x + 1, 23], fill=WOOD[3])
        im.alpha_composite(g, (0, gtop))
    if kind == 'timber' or cross:                       # half-timbered upper storeys (real Sheridan panels)
        for k, fh in enumerate(floors):
            yy = fy + sum(floors[:k])
            band = timber_band(w, min(fh, 16)); im.alpha_composite(band, (0, yy + max(0, fh - 16)))
            d.rectangle([0, yy, w - 1, yy + 1], fill=WOOD[1]); d.line([0, yy, w - 1, yy], fill=WOOD[3])
    # string course between floors
    for k in range(1, len(floors) + 1):
        yy = fy + sum(floors[:k]) - 1
        d.line([0, yy, w - 1, yy], fill=shade(wr[0] + (255,), 0.9)); d.line([0, yy + 1, w - 1, yy + 1], fill=wr[3] + (255,))
    # upper windows
    nwin = W
    for k, fh in enumerate(floors):
        yy = fy + sum(floors[:k])
        kindw = wins if not isinstance(wins, (list, tuple)) else wins[k % len(wins)]
        if kindw in ('arch', 'shlit', 'shdia'):
            sw = sprite(kindw).width; sh_ = sprite(kindw).height
        else:
            sw, sh_ = {'sash': (7, 10), 'tall': (7, 13), 'small': (6, 7), 'wide': (10, 8)}[kindw]
        if sh_ + 3 > fh: kindw, sw, sh_ = 'small', 6, 7
        slots = [int((i + 0.5) * w / nwin - sw / 2) for i in range(nwin)]
        for i, sx in enumerate(slots):
            if hoist and i == len(slots) // 2 and k == len(floors) - 1:
                d.rectangle([sx, yy + 2, sx + sw, yy + fh - 2], fill=WOOD[1], outline=DKW)        # loft loading door
                d.line([sx + 1, yy + 3, sx + 1, yy + fh - 3], fill=WOOD[3]); d.line([sx + sw // 2, yy + 3, sx + sw // 2, yy + fh - 3], fill=WOOD[0])
                continue
            window(im, sx, yy + max(2, (fh - sh_) // 2 - 1), kindw, wr, rng, shutters if shutters and kindw not in ('arch', 'shlit', 'shdia') else None, lit=lit and rng.random() < 0.5)
            if boxes and rng.random() < boxes:
                flowerbox(im, sx - 1, yy + max(2, (fh - sh_) // 2 - 1) + sh_ + 1, sw + 2, rng)
    # ---------------- ground floor: door, shop window, step
    dx = door * 16
    if shop:
        sx0, sx1 = (2, dx - 3) if door > 0 else (dx + 19, w - 3)
        if sx1 - sx0 >= 8:
            d.rectangle([sx0, gtop + 7, sx1, h - 4], fill=WOOD[1], outline=DKW)
            d.rectangle([sx0 + 1, gtop + 8, sx1 - 1, h - 6], fill=GLASS[1])
            for x in range(sx0 + 1, sx1, 4): d.line([x, gtop + 8, x, h - 6], fill=WOOD[1])
            d.line([sx0 + 1, gtop + 8, sx1 - 1, gtop + 8], fill=GLASS[3])
            goods = {'fish': [(200, 210, 220, 255), (150, 170, 186, 255)], 'bread': [(214, 160, 90, 255), (180, 120, 60, 255)],
                     'cloth': [(196, 60, 70, 255), (60, 110, 170, 255), (220, 190, 80, 255)], 'pots': [(160, 96, 60, 255), (110, 140, 90, 255)],
                     'books': [(120, 40, 40, 255), (40, 70, 110, 255), (60, 100, 60, 255)], 'masks': [(240, 232, 214, 255), (232, 190, 90, 255)]}.get(shop, FLOWERS)
            for x in range(sx0 + 2, sx1 - 1, 2): P(im, x, h - 7, rng.choice(goods)); P(im, x + (rng.random() < 0.5), h - 8, rng.choice(goods))
            d.line([sx0, h - 4, sx1, h - 4], fill=(220, 214, 204, 255))
            if not ('noawn' in str(shop)):
                awning(im, sx0 - 1, sx1 + 1, gtop + 1, rng.choice(AWN))
    else:
        for gx in range(0, W):                         # ground-floor windows away from the door
            if abs(gx - door) < 1 or (bigdoor and abs(gx - door) <= 1): continue
            window(im, gx * 16 + 5, gtop + 7, 'sash' if not lit else 'sash', wr, rng, shutters, lit=lit and rng.random() < 0.6)
    if bigdoor:                                        # warehouse cargo doors (2 tiles wide)
        bx0, bx1 = dx - 6, dx + 21
        d.rectangle([bx0, gtop + 3, bx1, h - 1], fill=WOOD[1], outline=DKW)
        d.pieslice([bx0, gtop - 1, bx1, gtop + 9], 180, 360, fill=WOOD[1], outline=DKW)
        for x in range(bx0 + 2, bx1, 3): d.line([x, gtop + 3, x, h - 2], fill=WOOD[2])
        d.line([bx0 + 1, gtop + 4, bx0 + 1, h - 2], fill=WOOD[3]); d.line([(bx0 + bx1) // 2, gtop + 3, (bx0 + bx1) // 2, h - 1], fill=WOOD[0])
        d.line([bx0 + 2, gtop + 12, bx1 - 2, gtop + 12], fill=D.IRON[1]); d.line([bx0 + 2, h - 6, bx1 - 2, h - 6], fill=D.IRON[1])
    else:
        dsp = sprite('apdoor') if kind in ('clap',) else sprite('shdoor') if kind == 'timber' or ground == 'timber' else None
        if dsp is not None and dsp.height <= 24:
            im.alpha_composite(dsp, (dx + 8 - dsp.width // 2, h - dsp.height))
        else:
            d.rectangle([dx + 3, gtop + 4, dx + 12, h - 1], fill=WOOD[1], outline=DKW)       # panelled door, stone frame
            d.pieslice([dx + 3, gtop + 1, dx + 12, gtop + 8], 180, 360, fill=WOOD[1], outline=DKW)
            d.line([dx + 4, gtop + 5, dx + 4, h - 2], fill=WOOD[3]); d.line([dx + 7, gtop + 5, dx + 7, h - 2], fill=WOOD[0])
            d.rectangle([dx + 5, gtop + 8, dx + 6, gtop + 12], outline=WOOD[2]); d.rectangle([dx + 9, gtop + 8, dx + 10, gtop + 12], outline=WOOD[2])
            P(im, dx + 10, gtop + 14, D.GOLD[2])
            d.line([dx + 2, gtop + 3, dx + 2, h - 1], fill=wr[3] + (255,)); d.line([dx + 13, gtop + 3, dx + 13, h - 1], fill=wr[0] + (255,))
        d.rectangle([dx + 2, h - 2, dx + 13, h - 1], fill=STONE[3] + (255,)); d.line([dx + 2, h - 1, dx + 13, h - 1], fill=STONE[1] + (255,))
    if sign:
        sx = dx + 15 if door < W - 1 else dx - 9
        bracket_sign(im, sx, gtop - 2, rng.choice(SHUT), sign, rng)
    # base course and corner quoins
    d.line([0, h - 1, w - 1, h - 1], fill=shade(wr[0] + (255,), 0.75))
    if quoin:
        for x, f in ((0, 1.08), (w - 3, 0.82)):
            for y in range(fy, h, 4):
                c = STONE[3] if (y // 4) % 2 == 0 else STONE[2]
                d.rectangle([x, y, x + 2, min(h - 1, y + 3)], fill=shade(c + (255,), f))
    d.line([0, fy, 0, h - 1], fill=OUT); d.line([w - 1, fy, w - 1, h - 1], fill=OUT)
    # ---------------- roof
    ry0 = 2; ry1 = fy                                   # roof spans rows [ry0, fy)
    rt = roof_tex(roof)
    if not gable:
        tile_fill(im, rt, (1, ry0, w - 1, ry1))
        span = max(1, ry1 - ry0)
        for y in range(ry0, ry1):                       # light near the ridge, darker toward the eaves; lit west end
            f = 1.10 - 0.28 * (y - ry0) / span
            shade_box(im, (1, y, w - 1, y + 1), f)
        shade_box(im, (1, ry0, 4, ry1), 1.06); shade_box(im, (w - 4, ry0, w - 1, ry1), 0.86)
        rr = RAMPS.get(roof.replace('_t', ''), RAMPS['terra']) if roof not in ('plank', 'plank_b', 'diamond') else RAMPS['umber']
        d.rectangle([1, ry0 - 2, w - 2, ry0 + 1], fill=shade(rr[3] + (255,), 1.0), outline=OUT)        # ridge cap
        d.line([2, ry0 - 1, w - 3, ry0 - 1], fill=rr[4] + (255,))
        d.line([0, ry0 - 2, 0, ry1], fill=OUT); d.line([w - 1, ry0 - 2, w - 1, ry1], fill=OUT)
        if cross:                                       # a cross gable over the middle bay
            gx0, gx1 = w // 2 - 12, w // 2 + 11
            gable_front(im, gx0, gx1, ry0 + 3, ry1, rt, roof, wr, kind, col, seed)
        for k in range(dormers):
            cx = int((k + 0.5) * w / dormers)
            dormer(im, cx - 5, ry0 + (ry1 - ry0) // 2 - 6, rt, wr)
    else:
        gable_front(im, 0, w - 1, ry0, ry1, rt, roof, wr, kind, col, seed, full=True)
        if hoist:                                       # hoist beam under the apex, rope and a hanging crate
            cx = w // 2
            d.rectangle([cx - 1, ry1 - 10, cx + 1, ry1 - 8], fill=WOOD[1], outline=DKW)
            d.line([cx, ry1 - 8, cx, fy + 10], fill=D.ROPED)
            d.rectangle([cx - 3, fy + 10, cx + 3, fy + 15], fill=WOOD[3], outline=DKW); d.line([cx - 2, fy + 12, cx + 2, fy + 12], fill=WOOD[1])
    # eave board and the shadow it casts on the facade
    d.rectangle([0, fy - 2, w - 1, fy], fill=WOOD[1] if roof not in ('slate', 'slate_t') else (70, 70, 84, 255), outline=OUT)
    d.line([1, fy - 1, w - 2, fy - 1], fill=WOOD[3] if roof not in ('slate', 'slate_t') else (120, 124, 140, 255))
    shade_box(im, (1, fy + 1, w - 1, fy + 4), 0.78); shade_box(im, (1, fy + 4, w - 1, fy + 5), 0.9)
    for c in chim:
        chimney(im, c * 16 + 5, max(0, ry0 - 1 + (rng.randrange(3) if not gable else 6)), 7)
    # ---------------- code rows: top row passable overhead, roof solid overhead, walls solid, door cell passable
    code = []
    for ty in range(H):
        if ty == 0: code.append('R' * W)
        elif ty * 16 < fy - 8: code.append('r' * W)
        else: code.append('W' * W)
    row = list(code[-1]); row[door] = 'D'; code[-1] = ''.join(row)
    return im, code, (door, H - 1)


def gable_front(im, x0, x1, ry0, ry1, rt, roof, wr, kind, col, seed, full=False):
    """a gable facing the street: two roof slopes meeting at a ridge running back (north), and the triangular
    gable wall at the front with bargeboards"""
    d = ImageDraw.Draw(im)
    cx = (x0 + x1) // 2; gw = (x1 - x0) // 2
    gh = min(ry1 - ry0 - 2, max(8, int(gw * 0.9)))      # gable triangle height
    gy = ry1 - gh                                     # apex y
    # slopes: rectangle from ry0 to the gable's sides; west lit, east shaded
    tile_fill(im, rt, (x0 + 1, ry0, x1, ry1))
    shade_box(im, (x0 + 1, ry0, cx, ry1), 1.08); shade_box(im, (cx, ry0, x1, ry1), 0.80)
    for y in range(ry0, ry1):
        shade_box(im, (x0 + 1, y, x1, y + 1), 1.0 - 0.12 * (y - ry0) / max(1, ry1 - ry0))
    rc = rt.getpixel((5, 1)); d.rectangle([cx - 1, ry0 - 1, cx + 1, gy], fill=shade(rc, 1.25)); d.line([cx + 1, ry0, cx + 1, gy], fill=shade(rc, 0.7))
    d.line([cx - 2, ry0, cx - 2, gy], fill=OUT); d.line([cx + 2, ry0, cx + 2, gy], fill=OUT)
    d.line([x0, ry0 - 1, x1, ry0 - 1], fill=OUT)
    # the gable wall triangle
    pts = [(x0 + 1, ry1), (cx, gy), (x1 - 1, ry1)]
    tri = Image.new('RGBA', im.size, CLEAR); td = ImageDraw.Draw(tri); td.polygon(pts, fill=(255, 255, 255, 255))
    if kind == 'clap': src = clapboard(col, im.width, im.height)
    elif kind == 'stone': src = ashlar(im.width, im.height, STONE, seed + 3)
    elif kind == 'brick': src = brick(im.width, im.height, seed + 3)
    else: src = plaster(col if kind != 'timber' else 'cream', im.width, im.height, seed + 3)
    m = tri.split()[3]
    im.paste(src, (0, 0), m)
    if kind == 'timber':                              # king post and braces in the gable
        d.line([cx, gy + 2, cx, ry1], fill=WOOD[1]); d.line([cx - gw // 2, ry1, cx, gy + 4], fill=WOOD[1]); d.line([cx + gw // 2, ry1, cx, gy + 4], fill=WOOD[1])
    # round or slit window in the gable
    wy = gy + gh // 2 - 1
    if gh >= 12:
        d.ellipse([cx - 3, wy - 2, cx + 3, wy + 4], fill=GLASS[1], outline=DKW); P(im, cx - 1, wy, GLASS[3]); d.line([cx, wy - 2, cx, wy + 4], fill=DKW)
    # bargeboards (lit west board, darker east board), finial
    d.line([x0, ry1, cx, gy - 1], fill=OUT, width=1); d.line([x0 + 1, ry1, cx, gy], fill=WOOD[3]); d.line([x0 + 2, ry1, cx, gy + 1], fill=WOOD[2])
    d.line([x1, ry1, cx, gy - 1], fill=OUT); d.line([x1 - 1, ry1, cx, gy], fill=WOOD[1]); d.line([x1 - 2, ry1, cx, gy + 1], fill=WOOD[0])
    d.line([cx, gy - 1, cx, gy - 4], fill=WOOD[0]); P(im, cx, gy - 5, D.GOLD[1])
    shade_box(im, (x0 + 2, ry1 - 1, x1 - 1, ry1), 0.85)


def dormer(im, x, y, rt, wr):
    d = ImageDraw.Draw(im)
    tile_fill(im, rt, (x, y, x + 11, y + 4)); shade_box(im, (x, y, x + 11, y + 4), 0.95)
    d.polygon([(x, y + 4), (x + 5, y - 1), (x + 10, y + 4)], fill=shade(rt.getpixel((3, 3)), 1.12), outline=OUT)
    d.rectangle([x + 1, y + 4, x + 9, y + 12], fill=wr[2] + (255,), outline=OUT)
    d.rectangle([x + 3, y + 5, x + 7, y + 11], fill=GLASS[1], outline=DKW); d.line([x + 5, y + 5, x + 5, y + 11], fill=DKW)
    P(im, x + 4, y + 6, GLASS[3])
    d.line([x + 1, y + 13, x + 9, y + 13], fill=(0, 0, 0, 70))


# ------------------------------------------------------------------ stairs, quay kit, harbour and street props
def stone_stairs(part, ramp=None):
    """dressed stone steps (1x1, repeats down a flight): pale treads with a lit nosing and a dark riser shadow,
    staggered joints; l / r pieces carry a cheek wall with a coping stone"""
    ramp = ramp or [(84, 76, 78), (128, 120, 114), (170, 162, 150), (204, 196, 182), (228, 222, 208)]
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    for k in range(4):
        y = k * 4
        d.line([0, y, 15, y], fill=ramp[4] + (255,)); d.line([0, y + 1, 15, y + 1], fill=ramp[3] + (255,))
        d.line([0, y + 2, 15, y + 2], fill=ramp[2] + (255,)); d.line([0, y + 3, 15, y + 3], fill=ramp[0] + (255,))
        for x in range((k * 5) % 7 + 2, 16, 7): P(im, x, y + 1, ramp[1] + (255,)); P(im, x, y + 2, ramp[1] + (255,))
    if part in 'lr':
        x = 0 if part == 'l' else 12
        d.rectangle([x, 0, x + 3, 15], fill=ramp[2] + (255,)); d.line([x + (0 if part == 'l' else 3), 0, x + (0 if part == 'l' else 3), 15], fill=OUT)
        d.line([x + 1 if part == 'l' else x, 0, x + 1 if part == 'l' else x, 15], fill=ramp[4] + (255,))
        d.line([x + 2 if part == 'l' else x + 2, 0, x + 2 if part == 'l' else x + 2, 15], fill=ramp[3] + (255,))
        inner = x + 4 if part == 'l' else x - 1
        d.line([inner, 0, inner, 15], fill=ramp[0] + (255,))
        for y in range(0, 16, 6): d.line([x, y, x + 3, y], fill=ramp[1] + (255,))
    return im


def timber_stairs(part):
    """plank steps between log posts (village / route): split-log treads, a lit edge, a dark riser"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    for k in range(4):
        y = k * 4
        d.line([0, y, 15, y], fill=WOOD[4]); d.line([0, y + 1, 15, y + 1], fill=WOOD[3])
        d.line([0, y + 2, 15, y + 2], fill=WOOD[2]); d.line([0, y + 3, 15, y + 3], fill=WOOD[0])
        for x in range(2 + (k % 2) * 4, 16, 8): P(im, x, y + 1, WOOD[2]); P(im, x + 1, y + 2, WOOD[1])
    if part in 'lr':
        x = 0 if part == 'l' else 13
        d.rectangle([x, 0, x + 2, 15], fill=WOOD[1], outline=OUT); d.line([x + 1, 0, x + 1, 15], fill=WOOD[3])
        for y in (1, 9): d.line([x, y, x + 2, y], fill=WOOD[0])
    return im


QY = [(64, 62, 68), (98, 94, 96), (134, 128, 124), (168, 160, 150), (198, 190, 176), (220, 214, 200)]


def quay(piece, v=0):
    """masonry quay kit (cliff-kit layout like Akuwa's): lip = coping course on the quay edge; f1 = ashlar face;
    f2 = face base with the wet band, weed and a foam line into the water; W / E = side copings; N = north rim"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im); rng = random.Random(hash((piece, v)) & 0xffff)
    kind, end = piece[:-1], piece[-1]          # end: w / m / e
    def blocks(y0, y1, course=5, wet=0):
        y = y0; k = 0
        while y < y1:
            x = -((k * 3 + v * 5) % 7)
            while x < 16:
                bw = 7 + ((x + k * 3 + v) % 3)
                c = QY[2] if rng.random() < 0.65 else QY[3] if rng.random() < 0.6 else QY[1]
                if wet and y + course > y1 - wet: c = (c[0] * 7 // 10, c[1] * 8 // 10, c[2] * 7 // 10)
                d.rectangle([x, y, x + bw - 1, min(y1 - 1, y + course - 1)], fill=c + (255,))
                d.line([x, y, x + bw - 2, y], fill=QY[3 if c != QY[3] else 4] + (255,))
                d.line([x + bw - 1, y, x + bw - 1, min(y1 - 1, y + course - 1)], fill=QY[0] + (255,))
                x += bw
            d.line([0, min(y1 - 1, y + course - 1), 15, min(y1 - 1, y + course - 1)], fill=QY[0] + (255,))
            y += course; k += 1
    if kind == 'lip':
        d.rectangle([0, 0, 15, 15], fill=QY[2] + (255,))
        d.rectangle([0, 0, 15, 9], fill=QY[4] + (255,)); d.line([0, 0, 15, 0], fill=QY[5] + (255,))   # coping stone (walkable top)
        for x in range(v * 3 % 8, 16, 8): d.line([x, 0, x, 9], fill=QY[2] + (255,))
        d.line([0, 9, 15, 9], fill=QY[1] + (255,)); d.line([0, 10, 15, 10], fill=QY[0] + (255,))
        blocks(11, 16, course=5)
    elif kind == 'f1':
        blocks(0, 16, course=5)
        if v == 1:                                          # an iron mooring ring
            d.ellipse([6, 4, 10, 9], outline=D.IRON[1]); P(im, 8, 3, D.IRON[2])
    elif kind == 'f2':
        blocks(0, 10, course=5, wet=4)
        for x in range(16):
            if rng.random() < 0.5: P(im, x, 9 - rng.randrange(3), (64, 104, 70, 255))
        d.rectangle([0, 10, 15, 11], fill=(44, 52, 60, 200))
        for x in range(16):
            if rng.random() < 0.55: P(im, x, 12, (230, 240, 246, 200))
            if rng.random() < 0.25: P(im, x, 13, (200, 222, 236, 150))
    elif kind in ('W', 'E'):                                # side coping strips (the quay runs north-south here)
        d.rectangle([0, 0, 15, 15], fill=CLEAR)
        x = 0 if kind == 'W' else 10
        d.rectangle([x, 0, x + 5, 15], fill=QY[4] + (255,))
        d.line([x + (0 if kind == 'W' else 5), 0, x + (0 if kind == 'W' else 5), 15], fill=QY[1] + (255,))
        d.line([x + (1 if kind == 'W' else 4), 0, x + (1 if kind == 'W' else 4), 15], fill=QY[5] + (255,) if kind == 'W' else QY[2] + (255,))
        for y in range(v * 3 % 7, 16, 7): d.line([x, y, x + 5, y], fill=QY[2] + (255,))
    elif kind == 'N':
        d.rectangle([0, 0, 15, 4], fill=QY[4] + (255,)); d.line([0, 4, 15, 4], fill=QY[1] + (255,)); d.line([0, 0, 15, 0], fill=QY[5] + (255,))
    if end in 'we' and kind in ('lip', 'f1', 'f2'):
        x = 0 if end == 'w' else 15
        d.line([x, 0, x, 15 if kind != 'f2' else 11], fill=OUT)
        d.line([x + (1 if end == 'w' else -1), 0, x + (1 if end == 'w' else -1), 15 if kind != 'f2' else 11], fill=QY[4] + (255,) if end == 'w' else QY[1] + (255,))
    return im


def crane():
    """a timber harbour crane (3x5): a plank housing with a treadwheel, a raking jib over the water, rope, hook and a
    slung crate.  Code: housing solid, jib overhead"""
    im = Image.new('RGBA', (48, 80), CLEAR); d = ImageDraw.Draw(im)
    # base platform and housing
    d.rectangle([4, 56, 30, 79], fill=WOOD[2], outline=OUT)
    for x in range(6, 30, 4): d.line([x, 57, x, 78], fill=WOOD[1])
    d.line([5, 57, 29, 57], fill=WOOD[4])
    d.rectangle([7, 36, 27, 58], fill=WOOD[2], outline=OUT)
    d.polygon([(5, 38), (17, 28), (29, 38)], fill=(120, 84, 62, 255), outline=OUT)
    d.line([7, 37, 17, 29], fill=(170, 130, 96, 255))
    d.ellipse([10, 41, 24, 55], outline=WOOD[0]); d.ellipse([11, 42, 23, 54], outline=WOOD[3])        # treadwheel
    for a in range(0, 180, 30):
        x1 = 17 + 6 * math.cos(math.radians(a)); y1 = 48 + 6 * math.sin(math.radians(a))
        d.line([17 - (x1 - 17), 48 - (y1 - 48), x1, y1], fill=WOOD[1])
    # jib: a raking beam from the housing up and east
    d.line([22, 34, 44, 4], fill=OUT, width=3); d.line([22, 33, 43, 4], fill=WOOD[3])
    d.line([26, 40, 44, 6], fill=OUT); d.line([26, 39, 43, 6], fill=WOOD[1])
    d.line([44, 4, 44, 50], fill=D.ROPED)                                     # rope
    d.line([42, 50, 46, 50], fill=D.IRON[1]); P(im, 44, 51, D.IRON[1])
    d.rectangle([39, 52, 47, 60], fill=WOOD[3], outline=DKW); d.line([40, 56, 46, 56], fill=WOOD[1]); d.line([43, 53, 43, 59], fill=WOOD[1])
    code = ['..O', '..O', 'OOO', 'WWO', 'WW.']
    return im, code


def salt_heap(v):
    """a raked heap of sea salt (2x2): bright cone, blue shadow side, a few crystals, a rake leaning on it"""
    im = Image.new('RGBA', (32, 32), CLEAR); d = ImageDraw.Draw(im)
    S = [(150, 164, 188, 255), (198, 210, 226, 255), (232, 238, 246, 255), (252, 252, 255, 255)]
    d.polygon([(2, 29), (15, 6 + v), (29, 29)], fill=S[2], outline=(120, 132, 156, 255))
    d.polygon([(15, 6 + v), (29, 29), (17, 29)], fill=S[1])
    d.line([4, 28, 15, 7 + v], fill=S[3])
    rng = random.Random(v)
    for _ in range(14): P(im, rng.randrange(6, 26), rng.randrange(14, 28), S[3] if rng.random() < 0.6 else S[0])
    d.line([2, 30, 29, 30], fill=(0, 0, 0, 60))
    if v % 2 == 0:
        d.line([22, 30, 30, 12], fill=WOOD[2]); d.line([28, 10, 31, 15], fill=WOOD[1])
    return im, ['OO', 'WW']


def morris():
    """a playbill column (1x2): a green iron column plastered with posters, a domed cap and finial"""
    im = Image.new('RGBA', (16, 32), CLEAR); d = ImageDraw.Draw(im)
    G = [(26, 62, 50, 255), (40, 92, 72, 255), (66, 128, 98, 255)]
    d.rectangle([3, 7, 12, 30], fill=G[1], outline=OUT)
    d.pieslice([2, 1, 13, 12], 180, 360, fill=G[2], outline=OUT); d.line([7, 1, 7, -2], fill=G[0]); P(im, 7, 0, D.GOLD[2])
    d.rectangle([2, 6, 13, 8], fill=G[2], outline=OUT)
    cols = [(240, 230, 206, 255), (214, 80, 74, 255), (232, 190, 90, 255), (120, 150, 200, 255), (244, 240, 230, 255)]
    rng = random.Random(7)
    y = 10
    for k in range(3):
        c = cols[k % len(cols)]
        d.rectangle([4, y, 11, y + 5], fill=c, outline=shade(c, 0.6))
        d.line([5, y + 2, 10, y + 2], fill=OUT if k != 1 else (250, 236, 200, 255)); P(im, 6 + rng.randrange(3), y + 4, (90, 60, 50, 255))
        y += 7
    d.line([4, 9, 4, 29], fill=G[2]); d.rectangle([2, 29, 13, 31], fill=G[0], outline=OUT)
    d.line([1, 31, 14, 31], fill=(0, 0, 0, 70))
    return im, ['O', 'W']


def playbill(v):
    """a poster pasted on a wall (1x1 decal over a facade)"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    c = [(240, 230, 206, 255), (214, 80, 74, 255), (232, 190, 90, 255), (120, 150, 200, 255)][v % 4]
    d.rectangle([4, 2, 11, 13], fill=c, outline=shade(c, 0.6))
    d.rectangle([5, 4, 10, 8], fill=[(150, 52, 52, 255), (40, 40, 60, 255), (120, 40, 40, 255), (240, 236, 220, 255)][v % 4])
    d.line([5, 10, 10, 10], fill=OUT); d.line([5, 12, 9, 12], fill=(100, 90, 80, 255))
    return im


def fountain():
    """the Saltmere fountain (5x4): an octagonal stone basin with water, a stepped plinth and a bronze Wailord
    rearing out of a wave, spouting.  Code: basin solid (rows 2-3), the statue's top overhead"""
    im = Image.new('RGBA', (80, 64), CLEAR); d = ImageDraw.Draw(im)
    W_ = [(46, 92, 150, 255), (70, 130, 190, 255), (120, 180, 226, 255), (200, 232, 248, 255)]
    pts = [(8, 30), (20, 22), (60, 22), (72, 30), (72, 50), (60, 58), (20, 58), (8, 50)]
    d.polygon(pts, fill=QY[3] + (255,), outline=OUT)                                        # basin rim
    inner = [(13, 32), (23, 26), (57, 26), (67, 32), (67, 48), (57, 53), (23, 53), (13, 48)]
    d.polygon(inner, fill=W_[1])
    for y in range(27, 53, 3):
        for x in range(15, 66, 6):
            if d.im.getpixel((x, y)) == W_[1][:3] + (255,) or True: P(im, x + (y % 6), y, W_[2])
    d.line([9, 31, 20, 23], fill=QY[5] + (255,)); d.line([20, 23, 59, 23], fill=QY[5] + (255,))
    d.line([8, 50, 20, 58], fill=QY[1] + (255,)); d.line([20, 58, 60, 58], fill=QY[0] + (255,)); d.line([60, 58, 72, 50], fill=QY[0] + (255,))
    # plinth
    d.rectangle([32, 30, 48, 46], fill=QY[2] + (255,), outline=OUT); d.line([33, 31, 47, 31], fill=QY[4] + (255,))
    d.rectangle([34, 24, 46, 32], fill=QY[3] + (255,), outline=OUT)
    # bronze Wailord on a wave
    B = [(60, 52, 40, 255), (104, 92, 64, 255), (150, 132, 88, 255), (190, 170, 120, 255)]
    d.ellipse([28, 6, 52, 26], fill=B[1], outline=OUT); d.chord([28, 6, 52, 26], 200, 340, fill=B[2])
    d.line([31, 12, 36, 8], fill=B[3]); P(im, 46, 14, OUT); d.arc([36, 16, 50, 24], 10, 170, fill=B[0])
    d.polygon([(28, 22), (22, 16), (30, 18)], fill=B[1], outline=OUT)
    for k, (sx, sy) in enumerate(((40, 5), (38, 2), (43, 1), (36, 0), (45, -1))):           # spout
        if sy >= 0: P(im, sx, sy, W_[3])
    d.arc([22, -6, 40, 14], 200, 300, fill=W_[3]); d.arc([40, -6, 58, 14], 240, 340, fill=W_[3])
    for x, y in ((24, 30), (56, 30), (22, 44), (58, 44)): P(im, x, y, W_[3]); P(im, x + 1, y + 1, W_[2])
    d.line([8, 60, 72, 60], fill=(0, 0, 0, 60))
    code = ['.OOO.', 'WWWWW', 'WWWWW', 'WWWWW']
    return im, code


def stall(cols, goods, seed):
    """a market stall (3x2): a striped canvas roof on poles over a plank counter with goods"""
    im = Image.new('RGBA', (48, 32), CLEAR); d = ImageDraw.Draw(im); rng = random.Random(seed)
    a, b = cols
    for x in range(2, 46):
        c = a if ((x - 2) // 4) % 2 == 0 else b
        d.line([x, 2, x, 11], fill=c + (255,)); P(im, x, 2, shade(c + (255,), 1.2))
    for x in range(2, 46, 4):
        d.polygon([(x, 12), (x + 2, 14), (x + 4, 12)], fill=(a if ((x - 2) // 4) % 2 == 0 else b) + (255,))
    d.rectangle([1, 1, 46, 12], outline=OUT)
    d.line([4, 13, 4, 30], fill=WOOD[1]); d.line([43, 13, 43, 30], fill=WOOD[1])
    d.rectangle([3, 20, 44, 30], fill=WOOD[2], outline=OUT); d.line([4, 21, 43, 21], fill=WOOD[4])
    for x in range(6, 42, 3):
        g = rng.choice(goods); P(im, x, 19, g); P(im, x + 1, 19, g); P(im, x, 18, shade(g, 1.15)); P(im, x + 1, 18, g)
    d.line([2, 31, 45, 31], fill=(0, 0, 0, 60))
    return im, ['OOO', 'WWW']


def lantern_string(v):
    """a string of paper lanterns across a street (1x1 overhead)"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    sag = lambda x: 2 + int(2 * math.sin(math.pi * ((x + v * 16) % 48) / 48.0))
    for x in range(16): P(im, x, sag(x), (60, 48, 40, 255))
    for lx in (3, 11):
        y = sag(lx) + 1; c = [(232, 70, 60, 255), (250, 200, 90, 255), (240, 130, 70, 255)][(lx + v) % 3]
        d.ellipse([lx - 2, y, lx + 2, y + 5], fill=c, outline=shade(c, 0.6)); P(im, lx - 1, y + 1, (255, 240, 200, 255))
    return im


def bollard(v):
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    d.rectangle([5, 5, 10, 14], fill=D.IRON[1], outline=OUT); d.rectangle([4, 3, 11, 6], fill=D.IRON[2], outline=OUT)
    d.line([6, 6, 6, 13], fill=D.IRON[2])
    if v: d.arc([1, 6, 9, 14], 90, 270, fill=D.ROPED); d.line([1, 10, 0, 15], fill=D.ROPED)
    d.line([4, 15, 11, 15], fill=(0, 0, 0, 70))
    return im


def rope_coil():
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    for r, c in ((6, D.ROPED), (5, D.ROPE), (3, D.ROPED), (2, D.ROPE)):
        d.ellipse([8 - r, 9 - r * 0.7, 8 + r, 9 + r * 0.7], outline=c)
    return im


def grass_tiles():
    """grass variation (map builder 8): Sheridan's 2x2 grass checker re-graded darker (shade patches under trees and
    along walls), a worn variant (trodden earth showing through, near doors and lanes), clover and tufts"""
    base = [[4832 + 647 - 384, 4832 + 646 - 384], [4832 + 655 - 384, 4832 + 654 - 384]]
    out = {}
    for i in range(2):
        for j in range(2):
            t = tex(base[i][j])
            cs = sorted(colours(t), key=lum)
            dark = ramp_map(t, [(38, 104, 70), (52, 128, 88), (70, 150, 104), (96, 172, 120)])
            out['gr_dark%d%d' % (i, j)] = dark
            worn = t.copy(); px = worn.load(); rng = random.Random(i * 2 + j)
            E = [(150, 128, 92, 255), (172, 150, 110, 255), (126, 106, 78, 255)]
            for _ in range(26):
                x, y = rng.randrange(16), rng.randrange(16)
                if (x + y * 3) % 5 < 3: px[x, y] = rng.choice(E)
            for _ in range(5):
                x, y = rng.randrange(1, 15), rng.randrange(1, 15)
                px[x, y] = E[1]; px[x + 1, y] = E[0]; px[x, y + 1] = E[2]
            out['gr_worn%d%d' % (i, j)] = worn
    return out


def clover(v):
    im = Image.new('RGBA', (16, 16), CLEAR); rng = random.Random(40 + v)
    for _ in range(4):
        cx, cy = rng.randrange(3, 13), rng.randrange(3, 13)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)):
            P(im, cx + dx, cy + dy, (58, 140, 76, 255) if (dx, dy) != (0, 0) else (90, 176, 98, 255))
        if v and rng.random() < 0.5: P(im, cx + 1, cy - 1, (240, 240, 250, 255))
    return im


def tuft(v):
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im); rng = random.Random(70 + v)
    bx = rng.randrange(4, 10); by = 12
    for k in range(5):
        x = bx + k - 2 + rng.randrange(-1, 2); hgt = 4 + rng.randrange(4)
        d.line([bx + 1, by, x, by - hgt], fill=(44, 112, 64, 255)); P(im, x, by - hgt, (110, 184, 104, 255))
    d.line([bx - 2, by + 1, bx + 4, by + 1], fill=(30, 80, 50, 120))
    return im


# ------------------------------------------------------------------ the catalogue
def townhouses():
    """the Saltmere catalogue: name -> (image, code, door).  Widths 3-7, one to three upper storeys, eaves and gable
    fronts, five roof and nine wall finishes, shops with awnings and signs.  Names: th_* houses, sp_* shops,
    wh_* warehouses."""
    out = {}
    U, T = [16], [14]
    spec = [  # name, W, roof_rows, floors, roof, wall, door, gable, extras
        ('th_a', 4, 3, [16, 16], 'terra', ('plaster', 'ochre'), 1, False, dict(chim=(3,), shutters=SHUT[0], boxes=0.5)),
        ('th_b', 3, 4, [16, 16], 'slate', ('plaster', 'white'), 1, True, dict(shutters=SHUT[1])),
        ('th_c', 5, 3, [16, 16], 'crimson', ('plaster', 'cream'), 2, False, dict(dormers=2, chim=(0, 4), boxes=0.6, shutters=SHUT[2])),
        ('th_d', 4, 3, [16], 'diamond', ('clap', 'native'), 2, False, dict(wins='arch', chim=(0,))),
        ('th_e', 3, 4, [16, 16, 14], 'terra', ('plaster', 'rose'), 1, True, dict(shutters=SHUT[3], boxes=0.4)),
        ('th_f', 4, 3, [16, 16], 'shingle', ('timber',), 1, False, dict(wins='shlit', ground='stone', chim=(3,))),
        ('th_g', 5, 4, [16, 16], 'slate_t', ('stone',), 2, True, dict(wins='tall', chim=(4,))),
        ('th_h', 3, 3, [16], 'umber_t', ('plaster', 'sky'), 1, False, dict(shutters=SHUT[3], boxes=0.7, chim=(2,))),
        ('th_i', 4, 4, [16, 16, 14], 'teal', ('plaster', 'salmon'), 2, True, dict(shutters=SHUT[0], boxes=0.3)),
        ('th_j', 6, 3, [16, 16], 'terra', ('plaster', 'sage'), 3, False, dict(cross=True, chim=(0, 5), shutters=SHUT[2], boxes=0.4)),
        ('th_k', 4, 3, [16, 16], 'shingle_m', ('brick',), 1, False, dict(wins='sash', chim=(3,), dormers=1)),
        ('th_l', 3, 4, [16, 16], 'crimson', ('clap', 'sky'), 1, True, dict(wins='arch')),
        ('th_m', 5, 3, [16], 'plank_b', ('timber',), 2, False, dict(wins='shdia', ground='timber', chim=(1,))),
        ('th_n', 4, 4, [16, 16], 'slate_t', ('plaster', 'lilac'), 2, True, dict(shutters=SHUT[1], boxes=0.5)),
        ('th_o', 3, 3, [16, 16], 'terra', ('plaster', 'white'), 1, False, dict(shutters=SHUT[0], chim=(0,))),
        ('th_p', 6, 4, [16, 16, 14], 'shingle', ('plaster', 'cream'), 2, False, dict(dormers=3, chim=(0, 5), shutters=SHUT[1])),
        ('th_q', 4, 3, [16], 'crimson', ('stone', 'sand'), 2, True, dict(wins='tall')),
        ('th_r', 5, 3, [16, 16], 'diamond', ('clap', 'sage'), 1, False, dict(wins='arch', cross=True)),
        # shops
        ('sp_fish', 4, 3, [16], 'slate', ('plaster', 'sky'), 3, False, dict(shop='fish', sign='fish', chim=(0,))),
        ('sp_bake', 4, 3, [16, 16], 'terra', ('plaster', 'ochre'), 0, False, dict(shop='bread', sign='mug', chim=(3,), boxes=0.5)),
        ('sp_cloth', 5, 4, [16, 16], 'crimson', ('plaster', 'rose'), 4, True, dict(shop='cloth', sign='key', shutters=SHUT[3])),
        ('sp_pots', 4, 3, [16], 'umber_t', ('timber',), 0, False, dict(shop='pots', sign='coin', ground='stone', wins='shlit')),
        ('sp_books', 3, 4, [16, 16], 'slate_t', ('plaster', 'sage'), 2, True, dict(shop='books', sign='key')),
        ('sp_masks', 4, 3, [16, 16], 'crimson', ('plaster', 'white'), 3, False, dict(shop='masks', sign='mask', boxes=0.5, shutters=SHUT[2])),
        ('sp_inn', 6, 4, [16, 16], 'terra', ('timber',), 2, False, dict(shop='bread', sign='mug', ground='stone', wins='shlit', dormers=2, chim=(0, 5))),
        ('sp_tav', 5, 3, [16, 16], 'plank', ('plaster', 'cream'), 1, False, dict(shop='pots', sign='mug', lit=True, shutters=SHUT[3], chim=(4,))),
        # warehouses (gable fronts with hoist beams; stone ground floor; big cargo doors)
        ('wh_a', 6, 5, [16, 16], 'shingle', ('brick',), 3, True, dict(ground='stone', hoist=True, bigdoor=True, wins='small')),
        ('wh_b', 7, 4, [16, 16], 'terra', ('plaster', 'ochre'), 3, True, dict(ground='stone', hoist=True, bigdoor=True, wins='small')),
        ('wh_c', 6, 4, [16], 'plank_b', ('timber',), 2, False, dict(ground='timber', bigdoor=True, wins='small', chim=())),
        ('wh_d', 7, 5, [16, 16], 'umber_t', ('stone', 'sand'), 3, True, dict(ground='stone', hoist=True, bigdoor=True, wins='small')),
    ]
    for i, (n, w, rr, fl, roof, wall, door, gable, ex) in enumerate(spec):
        im, code, dr = townhouse(w, rr, fl, roof=roof, wall=wall, door=door, gable=gable, seed=100 + i * 7, **ex)
        out[n] = (im, code, dr)
    return out


def city_pieces():
    """every city piece for rcustom (pieces_late3): name -> (image, code rows, door or None)"""
    out = {}
    for k in 'lmr':
        out['st_stair_' + k] = (stone_stairs(k), ['F'], None)
        out['tb_stair_' + k] = (timber_stairs(k), ['F'], None)
    for kind in ('lip', 'f1', 'f2'):
        for end in 'wme':
            for v in range(2 if end == 'm' else 1):
                out['qy_%s%s%d' % (kind, end, v)] = (quay(kind + end, v), ['Q' if kind == 'lip' else 'W'], None)
    for kind in ('W', 'E', 'N'):
        out['qy_%s0' % kind] = (quay(kind + 'm', 0), ['Q'], None)
    im, c = crane(); out['hb_crane'] = (im, c, None)
    for v in range(3):
        im, c = salt_heap(v); out['hb_salt%d' % v] = (im, c, None)
    im, c = morris(); out['pf_morris'] = (im, c, None)
    for v in range(4): out['pf_bill%d' % v] = (playbill(v), ['O'], None)
    im, c = fountain(); out['pf_fountain'] = (im, c, None)
    goods = [[(200, 210, 220, 255), (150, 170, 186, 255), (226, 120, 100, 255)], [(214, 160, 90, 255), (180, 120, 60, 255)],
             [(226, 74, 86, 255), (250, 220, 110, 255), (120, 190, 90, 255)], [(196, 60, 70, 255), (60, 110, 170, 255), (220, 190, 80, 255)],
             [(160, 96, 60, 255), (110, 140, 90, 255)]]
    for v in range(5):
        im, c = stall(AWN[v], goods[v], v); out['pf_stall%d' % v] = (im, c, None)
    for v in range(3): out['pf_lstring%d' % v] = (lantern_string(v), ['O'], None)
    for v in range(2): out['hb_bollard%d' % v] = (bollard(v), ['W'], None)
    out['hb_rope'] = (rope_coil(), ['W'], None)
    for n, im in grass_tiles().items(): out[n] = (im, ['G'], None)
    for v in range(2): out['gr_clover%d' % v] = (clover(v), ['F'], None)
    for v in range(3): out['gr_tuft%d' % v] = (tuft(v), ['F'], None)
    out.update(townhouses())
    return out


if __name__ == '__main__':
    ps = city_pieces()
    sel = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    ims = [(n, im.resize((im.width * 2, im.height * 2), Image.NEAREST)) for n, (im, c, dr) in ps.items() if not sel or n.startswith(tuple(sel))]
    Wd = 1900; x = y = 0; rowh = 0; pos = []
    for n, im in ims:
        if x + im.width > Wd: x = 0; y += rowh + 14; rowh = 0
        pos.append((n, im, x, y)); x += im.width + 10; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (Wd, y + rowh + 14), (150, 156, 150, 255))
    dr = ImageDraw.Draw(sheet)
    for n, im, x, y in pos:
        sheet.alpha_composite(im, (x, y + 12)); dr.text((x, y), n, fill=(120, 0, 80, 255))
    sheet.convert('RGB').save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/tdraw.png'); print(sheet.size)
