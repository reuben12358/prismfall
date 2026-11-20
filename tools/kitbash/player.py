"""Player characters (PLAYER_A = "Style A", PLAYER_B = "Style B"): battle fronts (80-px art, 160x160 export).
python3 -I tools/kitbash/player.py [variant ...]   (writes passes/pl_<v>.png and /tmp/pl.png)
Concept: OFF THE LAST FERRY. The kid who owns exactly one bag. Colourless (chalk white, undyed cream, ash, slate) with one
accent: the faded prism-teal canvas of a sea bag slung over one shoulder, a red ferry tag on its rope ("LAST CROSSING").
The bag is the signature: the biggest shape from behind in battle and on the map, and the arc ("they stop being carried
and choose what they carry").
  A1 body  : sd backpacker (BW class): hand rubbing the back of the head, the pack behind one shoulder
     pack  : -> canvas sea bag (recoloured, bedroll and straps cut, closed round bottom, cinched rope neck, ferry tag)
     head  : sd acetrainer-gen6 (flipped), hair repainted ash; the Backpacker's hand kept on top
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'PLAYER', '22_player.png'


def sd(n, flip=False):
    im = show.get_native('sd:' + n)[0]
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


# ---------------------------------------------------------------- palette
P = {'k': BLACK,
     # ash hair (cool grey-beige), light -> dark
     'a1': H('e4e0d8'), 'a2': H('c4beb4'), 'a3': H('9a938a'), 'a4': H('6a645e'),
     # chalk white jacket (cool)
     'w1': H('f8f8f8'), 'w2': H('d8dce6'), 'w3': H('a8aebe'), 'w4': H('6c7286'),
     # slate (tee, trousers)
     's1': H('8a92a4'), 's2': H('646b7c'), 's3': H('434856'), 's4': H('2a2d38'),
     # faded prism-teal canvas (sea bag)
     't1': H('b8e4dc'), 't2': H('7ec4ba'), 't3': H('4e9890'), 't4': H('2c6464'), 't5': H('1a3e44'),
     # rope, tag
     'r1': H('e8d8b0'), 'r2': H('b89c70'), 'r3': H('7a6448'), 'g1': H('f04c3c'), 'g2': H('a82c2c'), 'p1': H('fff4dc'),
     # boots
     'b1': H('7a5a44'), 'b2': H('523a2e'), 'b3': H('30221c')}
X = {'k': BLACK, 'a': P['a1'], 'A': P['a2'], 'B': P['a3'], 'C': P['a4'], 'r': P['r1'], 'R': P['r2'], 'q': P['r3'],
     'g': P['g1'], 'G': P['g2'], 'p': P['p1'], 't': P['t1'], 'T': P['t2'], 'u': P['t3'], 'U': P['t4'], 'v': P['t5'],
     'w': P['w1'], 'W': P['w2'], 'x': P['w3'], 'X': P['w4'], 's': H('f8d0b8'), 'S': H('d8a078')}


def ramp(src_cols, dst):
    return mat.lumrank_map(src_cols, dst)


# ---------------------------------------------------------------- A1: the backpacker body
BP_PACK = [(44, 16), (52, 16), (64, 22), (65, 64), (44, 64), (50, 46), (45, 36)]   # pack polygon (hand excluded later)
BP_HAND = [(17, 18), (21, 12), (25, 7), (30, 6), (31, 10), (31, 19), (30, 27), (27, 33), (20, 33), (17, 25)]


def sea_bag_from_pack(b, pack_r, cut_y, bottom, ctr, rx):
    """the pack above cut_y becomes the bag's top; each column is extended down to an elliptical round bottom
    (centre x ctr, half-width rx, lowest row bottom); outlined; returned as its own layer."""
    W, Hh = b.size
    bag = mat.keep(b, pack_r)
    q = bag.load()
    for y in range(cut_y, Hh):
        for x in range(W):
            q[x, y] = CLEAR
    for x in range(W):
        col = [q[x, y] for y in range(cut_y - 4, cut_y) if q[x, y][3] and q[x, y] != BLACK]
        if not col:
            continue
        dx = (x - ctr) / float(rx)
        if abs(dx) >= 1:
            continue
        yb = int(round(bottom - (bottom - cut_y) * (1 - (1 - dx * dx) ** 0.5) * 1.6))
        for y in range(cut_y, max(cut_y, yb)):
            q[x, y] = col[(y - cut_y) % len(col)] if y < yb - 2 else col[0]
    bag = mat.clean_orphans(bag)
    return mat.outline_outer(bag, BLACK)


PACK_COLS = {H('60b0c8'), H('587098'), H('383060'), H('a8b0b0'), H('f8f8f8'), H('d85838'), H('784858')}
SKIN = {H('f8d0b8'), H('d8a078'), H('b87860')}


def strip_pack(b, poly, cols):
    """erase the pack: its colours inside poly, then the outline pixels left touching nothing of the body."""
    reg = mat.region(b.size, [poly]).load()
    out = b.copy(); p = out.load(); W, Hh = b.size
    for y in range(Hh):
        for x in range(W):
            if reg[x, y] and p[x, y] in cols:
                p[x, y] = CLEAR
    for _ in range(2):
        kill = []
        for y in range(Hh):
            for x in range(W):
                if reg[x, y] and p[x, y] == BLACK:
                    body = any(0 <= x + dx < W and 0 <= y + dy < Hh and p[x + dx, y + dy][3] and p[x + dx, y + dy] != BLACK
                               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if not body:
                        kill.append((x, y))
        for (x, y) in kill:
            p[x, y] = CLEAR
    return mat.clean_orphans(out)


def head_swap(body, head_src, head_poly, dx, dy, erase_poly, top=None):
    """erase the base head (erase_poly), paste the donor head (head_poly of head_src, moved dx,dy) and put the layer
    top (e.g. a hand in the hair) back on top."""
    out = mat.erase(body, mat.region(body.size, [erase_poly]))
    head = mat.keep(head_src, mat.region(head_src.size, [head_poly]))
    out = mat.paste(out, head, dx, dy)
    if top is not None:
        out = mat.paste(out, top, 0, 0)
    return out


ASH = {H('a1cb75'): P['a2'], H('73984f'): P['a3'], H('3b561f'): P['a4']}          # acetrainer-gen6 hair -> ash


def hand_layer(b, poly, cols):
    """pixels of b inside poly whose colour is in cols, plus the black outline touching them."""
    reg = mat.region(b.size, [poly]).load(); p = b.load(); W, Hh = b.size
    out = Image.new('RGBA', b.size, CLEAR); q = out.load()
    for y in range(Hh):
        for x in range(W):
            if reg[x, y] and p[x, y] in cols:
                q[x, y] = p[x, y]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < W and 0 <= y + dy < Hh and p[x + dx, y + dy] == BLACK:
                        q[x + dx, y + dy] = BLACK
    return out


def sea_bag():
    """the sea bag alone (cropped): the Backpacker's pack recoloured to teal canvas, extended to a round bottom, with a
    cinched rope neck and the red ferry tag. Returns (layer, (x0, y0)) where (x0, y0) is its place on the Backpacker."""
    b = sd('backpacker')
    pack_r = mat.region(b.size, [BP_PACK])
    p = b.load(); pr = pack_r.load()
    for y in range(b.size[1]):
        for x in range(b.size[0]):
            if pr[x, y] and p[x, y] in SKIN:
                pr[x, y] = 0
    TEAL = {H('f8f8f8'): P['t1'], H('a8b0b0'): P['t2'], H('60b0c8'): P['t2'], H('587098'): P['t3'], H('383060'): P['t4'],
            H('d85838'): P['t3'], H('784858'): P['t4']}
    bag = sea_bag_from_pack(mat.recolour(b, TEAL, pack_r), pack_r, 39, 52, 53, 9)
    # the hand's skin hole: fill it with canvas from the column above
    q = bag.load()
    for x in range(44, 60):
        last = None
        for y in range(17, 53):
            c = q[x, y]
            if c[3] and c != BLACK:
                last = c
            elif not c[3] and last is not None and any(q[x, yy][3] for yy in range(y + 1, 53)):
                q[x, y] = last
    bag = mat.erase(bag, mat.region(bag.size, rect=(59, 38, 63, 46)))
    bag = sea_bag_neck(bag, 47, 12)
    bb = kb.bbox(bag)
    bag = bag.crop(bb)
    # close the left side (hidden behind the Backpacker's body): a straight seam from under the neck to the bottom,
    # canvas filled in from the seam, stray outline bits inside the bag turned to canvas shadow
    q = bag.load(); w, h = bag.size
    for y in range(8, h - 2):
        xl = int(round(1 + (y - 8) * 5.0 / (h - 11)))
        xs = [x for x in range(w) if q[x, y][3] and q[x, y] != BLACK]
        if not xs:
            continue
        xf = xs[0]
        for x in range(xl, xf):
            q[x, y] = BLACK if x == xl else (P['t4'] if x == xl + 1 else P['t3'])
        for x in range(xl + 1, w - 1):
            if q[x, y] == BLACK and q[x - 1, y][3] and q[x + 1, y][3] and q[x - 1, y] != BLACK and q[x + 1, y] != BLACK:
                q[x, y] = P['t4']
        for x in range(0, xl):
            q[x, y] = CLEAR
    return bag, (bb[0], bb[1])


def a1():
    b = sd('backpacker')
    # --- sea bag layer from the pack
    pack_r = mat.region(b.size, [BP_PACK])
    p = b.load(); pr = pack_r.load()
    for y in range(b.size[1]):
        for x in range(b.size[0]):
            if pr[x, y] and p[x, y] in SKIN:
                pr[x, y] = 0
    TEAL = {H('f8f8f8'): P['t1'], H('a8b0b0'): P['t2'], H('60b0c8'): P['t2'], H('587098'): P['t3'], H('383060'): P['t4'],
            H('d85838'): P['t3'], H('784858'): P['t4']}
    bag = sea_bag_from_pack(mat.recolour(b, TEAL, pack_r), pack_r, 39, 52, 53, 9)
    body = strip_pack(b, BP_PACK, PACK_COLS)
    out = mat.under(body, bag, 0, 0)
    # --- head: acetrainer-gen6, flipped, eyes on the Backpacker's eyes; his hand stays in the hair
    at = mat.recolour(sd('acetrainer-gen6', flip=True), ASH)
    hand = hand_layer(b, BP_HAND, SKIN | {H('60b0c8'), H('587098'), H('383060'), H('784858')})
    out = head_swap(out, at, [(26, 3), (49, 3), (49, 21), (40, 22), (40, 25), (33, 25), (33, 22), (26, 21)], -3, 0,
                    [(28, 2), (48, 2), (48, 16), (44, 17), (43, 22), (38, 25), (31, 25), (29, 20)], hand)
    out = mat.recolour(out, {H('d85838'): P['t3']}, mat.region(out.size, rect=(44, 16, 64, 62)))
    out = mat.erase(out, mat.region(out.size, rect=(59, 38, 63, 46)))                 # strap ends
    out = mat.patch(out, 58, 38, ['.', 'k'], X)
    # --- outfit: chalk-white jacket, slate tee, teal trim, charcoal trousers, boots
    bodyr = mat.mask_not(mat.colour_mask(out, [P[k] for k in ('t1', 't2', 't3', 't4', 't5')]))
    out = mat.recolour(out, {H('f8f8f8'): P['s3'], H('a8b0b0'): P['s4'], H('d85838'): P['t2']},
                       mat.region(out.size, rect=(28, 22, 52, 50)))
    out = mat.recolour(out, {H('60b0c8'): P['w1'], H('587098'): P['w3'], H('383060'): P['w4']}, bodyr)
    out = mat.recolour(out, {H('687858'): P['s1'], H('505048'): P['s2'], H('485040'): P['s2'], H('383028'): P['s3']},
                       mat.region(out.size, rect=(20, 46, 56, 73)))
    out = mat.recolour(out, {H('f8d0b8'): P['b1'], H('d8a078'): P['b1'], H('b87860'): P['b2'], H('784858'): P['b3'],
                             H('383028'): P['b3'], H('687858'): P['s3'], H('505048'): P['s3'], H('485040'): P['s4']},
                       mat.region(out.size, rect=(20, 73, 56, 80)))
    out = sea_bag_neck(out, 47, 12)
    return out


def sea_bag_neck(im, x, y):
    """cinched canvas neck, a rope wrap and a red ferry tag ('LAST CROSSING') hanging from it."""
    im = mat.patch(im, x - 2, y, ['..kkk...',
                                  '.kTtTk..',
                                  '.kuTuk..',
                                  '..krRkk.',
                                  '.kRrRqk.',
                                  'kuTTTuUk'], X)
    return mat.patch(im, x + 3, y + 5, ['.q.', 'kGk', 'ggg', 'gpg', 'GGG', 'kkk'], dict(X, g=P['g1'], G=P['g2']))


# ---------------------------------------------------------------- B1: the snow ace trainer's stance, hair in the wind
SNOW_HAIR = {H('5a7b73'): P['a1'], H('414a52'): P['a2'], H('312931'): P['a4']}
SNOW_BOOT = {H('5a7b73'): P['b1'], H('414a52'): P['b2'], H('312931'): P['b3']}
FUR_TEAL = {H('e6debd'): P['t1'], H('b4ac83'): P['t3'], H('524a41'): P['t4']}
FUR_GLOVE = {H('e6debd'): P['s1'], H('b4ac83'): P['s2'], H('524a41'): P['s3']}
FUR_CUFF = {H('e6debd'): P['b1'], H('b4ac83'): P['b2'], H('524a41'): P['b3']}


def snow_outfit(b, belt_y=42, waist=45):
    R = lambda *r: mat.region(b.size, rect=r)
    b = mat.recolour(b, SNOW_HAIR, R(0, 0, 79, 36))
    b = mat.recolour(b, {H('414a52'): P['s3'], H('5a7b73'): P['s2'], H('312931'): P['s4']}, R(0, 37, 79, 58))   # belt
    b = mat.recolour(b, SNOW_BOOT, R(0, 59, 79, 79))
    b = mat.recolour(b, {H('e68b41'): P['w1'], H('ac6a41'): P['w3']}, R(0, 0, 79, waist - 1))
    b = mat.recolour(b, {H('e68b41'): P['s1'], H('ac6a41'): P['s2']}, R(0, waist, 79, 79))
    b = mat.recolour(b, FUR_GLOVE, R(0, 20, 26, 40))
    b = mat.recolour(b, FUR_GLOVE, R(48, 30, 79, 46))
    b = mat.recolour(b, FUR_TEAL, R(26, 24, 47, 36))
    b = mat.recolour(b, FUR_CUFF, R(0, 56, 79, 70))
    return b


def b1():
    b = sd('acetrainersnowf')
    b = snow_outfit(b)
    bag, _ = sea_bag()
    return mat.under(b, mat.flip(bag), 13, 12)


def a2():
    b = sd('acetrainersnow')
    at = mat.recolour(sd('acetrainer-gen6'), ASH)
    b = head_swap(b, at, [(53, 3), (30, 3), (30, 21), (39, 22), (39, 25), (46, 25), (46, 22), (53, 21)], -7, 2,
                  [(26, 5), (49, 5), (49, 24), (40, 26), (32, 27), (28, 24), (26, 14)])
    b = mat.recolour(b, FUR_GLOVE, mat.region(b.size, rect=(8, 34, 31, 54)))           # the low ball hand
    b = snow_outfit(b)
    bag, _ = sea_bag()
    return mat.under(b, mat.flip(bag), 13, 12)


# ---------------------------------------------------------------- B2: hello, I'm new here (hiker-gen9, waving)
def b2():
    b = sd('hiker-gen9')
    R = lambda *r: mat.region(b.size, rect=r)
    PACKC = {H('408f9c'), H('20474d'), H('87dbd1'), H('505050'), H('302d2b'), H('d5def5'), H('d9ceb2'), H('e79565'),
             H('72432a'), H('574322'), H('afbcda'), H('6a7ea6')}
    b = strip_pack(b, [(50, 19), (58, 19), (58, 43), (50, 43)], PACKC)
    b = mat.recolour(b, {H('f4d7a6'): P['a1'], H('9a7b46'): P['a2'], H('574322'): P['a4'], H('724637'): P['a3']},
                     R(30, 4, 56, 34))
    b = mat.recolour(b, {H('505048'): P['t3'], H('302d2b'): P['t4'], H('e79565'): P['t2']}, R(30, 4, 56, 15))  # cap band
    b = mat.recolour(b, {H('d5def5'): P['w1'], H('afbcda'): P['w2'], H('6a7ea6'): P['w3'], H('42526f'): P['w4']},
                     R(20, 24, 58, 44))
    b = mat.recolour(b, {H('e79565'): P['s2'], H('b36839'): P['s3']}, R(30, 24, 52, 44))
    b = mat.recolour(b, {H('d9ceb2'): P['s1'], H('9e8f69'): P['s2'], H('505050'): P['s3'], H('302d2b'): P['s4']},
                     R(25, 36, 60, 68))
    b = mat.recolour(b, {H('757568'): P['b1'], H('302d2b'): P['b3'], H('505050'): P['b2'], H('e6945a'): P['b1'],
                         H('b36839'): P['b2'], H('9c6b52'): P['b2'], H('72432a'): P['b3']}, R(25, 68, 60, 80))
    bag, _ = sea_bag()
    return mat.under(b, bag, 44, 14)


def build(var='A1'):
    return {'A1': a1, 'A2': a2, 'B1': b1, 'B2': b2}[var]()


if __name__ == '__main__':
    vs = sys.argv[1:] or ['A1']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/pl_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/pl.png')
    kb.grid(ims[0], k=10).save('/tmp/pl_grid.png')
