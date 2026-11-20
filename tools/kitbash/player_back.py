"""Player battle backs for EBDX, in the base project's player-back format: 5 frames (idle, wind-up, throw x3) side by side,
each 160x234 (80x117 art doubled) -> file 800x234, like Graphics/Trainers/POKEMONTRAINER_Red_back.png. EBDX shows frame 0,
then steps src_rect.x by width/5 during the send-out (Battler Sendout Player.rb).
  A: body + throw = the base project's Red big back (5 frames); head = Rejuvenation trback001 (back of a messy head with a
     scarf), hair -> ash, scarf -> teal; vest -> chalk-white jacket, black tee -> slate, jeans -> slate, yellow pack -> teal
     canvas with the red ferry tag.
  B: body + throw = Leaf big back; hat -> hair (her own hair continued), brown hair -> ash; tank -> white jacket, skirt ->
     slate, satchel -> teal canvas + tag.
python3 -I tools/kitbash/player_back.py [A|B]  -> /tmp/plb_<k>.png (strip x3) and passes/plb_<k>_native.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, backstrips as bs, player as pl
from mat import H, CLEAR, BLACK
from PIL import Image

P, X = pl.P, pl.X


def align(tmpl, im, box, rng=(-12, 40, -6, 32)):
    """offset (dx, dy) where the template's opaque pixels inside box best match im's pixels."""
    tp = tmpl.load(); ip = im.load(); W, Hh = im.size
    pts = [(x, y, tp[x, y]) for y in range(box[1], box[3]) for x in range(box[0], box[2]) if tp[x, y][3]]
    best = (-1, 0, 0)
    for dy in range(rng[2], rng[3]):
        for dx in range(rng[0], rng[1]):
            s = 0
            for x, y, c in pts:
                xx, yy = x + dx, y + dy
                if 0 <= xx < W and 0 <= yy < Hh and ip[xx, yy] == c:
                    s += 1
            if s > best[0]:
                best = (s, dx, dy)
    return best[1], best[2]


RED_CAP = {H('e2372e'), H('b62018'), H('931a13'), H('c02f2f'), H('f65f3f'), H('eeeeee'), H('cbc2b9'), H('a8978e'),
           H('b19f97'), H('8e867e'), H('755d55'), H('454545'), H('2e2e27'), H('191919'), H('050505'), H('101010'),
           H('65452e'), H('452719'), H('703737'), H('562618'), H('833a25'), H('af4f32'), H('362720'), H('403020'),
           H('6d6d65'), H('202020'), H('806860'), H('b0a098'), H('f7f7ee'), H('f8f8f0'), H('c8c0a8')}
RED_HAIR = {H('65452e'), H('452719'), H('703737'), H('562618'), H('833a25'), H('362720'), H('403020')}
RED_SKIN = {H('f7d4a8'), H('f7d4b9'), H('f8d8b0'), H('c2b99f'), H('b97a57')}
RED_HEAD0 = [(3, 8), (48, 8), (48, 33), (41, 45), (32, 49), (16, 49), (9, 42), (3, 37)]
RED_FACE0 = (29, 28, 40, 46)

RJ_HAIR = {H('79564e'): P['a2'], H('573d38'): P['a3'], H('3b2a26'): P['a4'], H('2f211e'): P['a4'], H('9c7666'): P['a2']}
RJ_SCARF = {H('8eae8b'): P['t1'], H('519d5f'): P['t2'], H('367b4f'): P['t3'], H('1d5d45'): P['t4'], H('0e3d3b'): P['t5']}

RED_OUTFIT = {H('e2372e'): P['w1'], H('f65f3f'): P['w1'], H('c02f2f'): P['w2'], H('b62018'): P['w3'], H('931a13'): P['w4'],
              H('eeeeee'): P['w2'], H('cbc2b9'): P['w3'], H('a8978e'): P['w3'], H('b19f97'): P['w3'], H('8e867e'): P['w4'],
              H('454545'): P['s3'], H('2e2e27'): P['s4'], H('2e3636'): P['s4'], H('6d6d65'): P['s2'],
              H('6db9dc'): P['s1'], H('4d7e97'): P['s2'], H('204d75'): P['s3'], H('192e45'): P['s4'],
              H('ffda4f'): P['t2'], H('ffeca4'): P['t1'], H('c7932f'): P['t3'], H('866d39'): P['t4'], H('5b4315'): P['t5']}


def back_a():
    fr = bs.frames('EB:POKEMONTRAINER_Red_back')
    head = bs.frames('RJ:trback001')[0]
    head = mat.keep(head, mat.region(head.size, [[(6, 6), (40, 6), (40, 36), (37, 46), (12, 46), (12, 38), (6, 34)]]))
    head = mat.recolour(mat.recolour(head, RJ_HAIR), RJ_SCARF)
    # the template for alignment: frame 0's cap (its upper half only, which keeps its shape across frames)
    tmpl = mat.keep(fr[0], mat.region(fr[0].size, rect=(12, 10, 42, 22)))
    out = []
    for i, f in enumerate(fr):
        dx, dy = (0, 0) if i == 0 else align(tmpl, f, (12, 10, 42, 22))
        reg = mat.region(f.size, [[(x + dx, y + dy) for x, y in RED_HEAD0]]).load()
        fx = (RED_FACE0[0] + dx, RED_FACE0[1] + dy, RED_FACE0[2] + dx, RED_FACE0[3] + dy)
        prot = {1: (0, 14, 22, 60), 2: (14, 14, 29, 29)}.get(i)     # the raised ball hand, left of the head
        g = f.copy(); p = g.load()
        for y in range(f.size[1]):
            for x in range(f.size[0]):
                c = p[x, y]
                if prot and prot[0] <= x <= prot[2] and prot[1] <= y <= prot[3] and c not in RED_HAIR:
                    continue
                if reg[x, y] and (c in RED_CAP or (c in RED_SKIN and fx[0] <= x <= fx[2] and fx[1] <= y <= fx[3])):
                    p[x, y] = CLEAR
        g = mat.recolour(g, RED_OUTFIT)
        g = mat.paste(g, head, 2 + dx, 4 + dy)
        out.append(mat.drop_specks(mat.clean_orphans(g)))
        print('frame', i, 'head offset', dx, dy)
    return out


LEAF_HAT = {H('b9b9db'), H('ede5ff'), H('ffffff'), H('f8f8f8'), H('f0f0f0'), H('d0c8c0'), H('c04040'), H('a62828'),
            H('ca5544'), H('ff6554'), H('f86058'), H('707068'), H('525252'), H('787870'), H('989088'), H('989080'),
            H('b8a8a0'), H('101010'), H('080808'), H('000000'), H('282020'), H('384040')}
LEAF_HAIR = {H('855544'): P['a2'], H('543626'): P['a4'], H('684840'): P['a3'], H('785850'): P['a3'], H('403030'): P['a4'],
             H('604830'): P['a3'], H('403028'): P['a4']}
LEAF_GOLD = {H('a87536'), H('f8c058')}
LEAF_HEAD0 = [(9, 10), (53, 10), (53, 36), (44, 36), (40, 30), (14, 36), (9, 33)]
LEAF_SKIN = [H('f8d8c0'), H('c89070'), H('c0a090'), H('e8c0a8'), H('d0a088')]
LEAF_OUTFIT = {H('78b8d8'): P['w1'], H('90a0b8'): P['w2'], H('5088b0'): P['w3'], H('182850'): P['w4'],
               H('f86058'): P['s1'], H('ff6554'): P['s1'], H('e07080'): P['s1'], H('ca5544'): P['s2'], H('c04040'): P['s2'],
               H('a85860'): P['s2'], H('a62828'): P['s3']}
RJ2_HAIR = {H('d7639d'): P['a2'], H('ff9db4'): P['a1'], H('ba4b82'): P['a3'], H('98356b'): P['a4'], H('692057'): P['a4'],
            H('440a36'): P['a4']}


def skin_parts(f, skin, face_box):
    """recolour skin by part: legs (low) -> slate leggings, small pieces (hands past the wristbands) -> grey gloves,
    other limbs -> white sleeves; the face (inside face_box) stays."""
    p = f.load(); w, h = f.size; seen = set(); sk = set(skin)
    L = sorted(sk, key=kb.lum)
    for y in range(h):
        for x in range(w):
            if (x, y) in seen or p[x, y] not in sk:
                continue
            comp = []; st = [(x, y)]; seen.add((x, y))
            while st:
                cx, cy = st.pop(); comp.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and p[nx, ny] in sk:
                        seen.add((nx, ny)); st.append((nx, ny))
            ys = [c[1] for c in comp]; xs = [c[0] for c in comp]
            cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
            if face_box[0] <= cx <= face_box[2] and face_box[1] <= cy <= face_box[3]:
                continue
            if min(ys) >= 78:
                ramp = [P['s3'], P['s2'], P['s1']]
            elif len(comp) < 45:
                ramp = [P['s3'], P['s2'], P['s1']]
            else:
                ramp = [P['w3'], P['w2'], P['w1']]
            for (qx, qy) in comp:
                c = p[qx, qy]
                k = 2 if kb.lum(c) > 200 else (1 if kb.lum(c) > 150 else 0)
                p[qx, qy] = ramp[k]
    return f


def back_b():
    fr = bs.frames('EB:POKEMONTRAINER_Leaf_back')
    head = bs.frames('RJ:trback002')[0]
    head = mat.keep(head, mat.region(head.size, [[(12, 15), (50, 15), (50, 44), (44, 48), (38, 50), (20, 52), (12, 48)]]))
    head = mat.recolour(head, RJ2_HAIR)
    tmpl = mat.keep(fr[0], mat.region(fr[0].size, rect=(14, 12, 48, 26)))
    bag, _ = pl.sea_bag()
    out = []
    for i, f in enumerate(fr):
        dx, dy = (0, 0) if i == 0 else align(tmpl, f, (14, 12, 48, 26), (-12, 40, -6, 40))
        reg = mat.region(f.size, [[(x + dx, y + dy) for x, y in LEAF_HEAD0]]).load()
        g = f.copy(); p = g.load()
        prot = {1: (0, 8, 12, 60), 2: (8, 6, 26, 32)}.get(i)
        for y in range(f.size[1]):
            for x in range(f.size[0]):
                if prot and prot[0] <= x <= prot[2] and prot[1] <= y <= prot[3]:
                    if i == 1 and p[x, y] not in (H('b9b9db'), H('ede5ff'), H('d0c8c0')):
                        continue
                    if i == 2 and (p[x, y] in LEAF_SKIN or p[x, y] in (H('ffffff'), H('f0f0f0'), H('f8f8f8'))):
                        continue
                if reg[x, y] and p[x, y] in LEAF_HAT:
                    p[x, y] = CLEAR
        # gold: hair highlight next to brown hair, else the satchel (-> teal canvas)
        q = g.copy().load()
        for y in range(f.size[1]):
            for x in range(f.size[0]):
                if q[x, y] in LEAF_GOLD:
                    near = any(0 <= x + a < f.size[0] and 0 <= y + b < f.size[1] and q[x + a, y + b] in LEAF_HAIR
                               for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2))
                    p[x, y] = (P['a1'] if q[x, y] == H('f8c058') else P['a2']) if near else \
                        (P['t2'] if q[x, y] == H('f8c058') else P['t3'])
        g = mat.recolour(g, LEAF_HAIR)
        g = skin_parts(g, LEAF_SKIN, (30 + dx, 26 + dy, 50 + dx, 52 + dy))
        g = mat.recolour(g, LEAF_OUTFIT)
        g = mat.paste(g, head, -3 + dx, -2 + dy)
        g = mat.paste(g, bag, 37 + dx + BAG_B[i][0], 44 + dy + BAG_B[i][1])     # the sea bag on her back
        if i == 2:
            g = mat.outline_outer(g, BLACK)
            # the ball shares the hat's whites and went with it: put the original ball (and its outline) back on top
            op = f.load(); whites = [(x, y) for y in range(6, 33) for x in range(6, 28)
                                     if op[x, y] in (H('ffffff'), H('f0f0f0'), H('f8f8f8'), H('ede5ff'))]
            near = [(x, y) for (x, y) in whites if any(op[x + a, y + b] in LEAF_SKIN for a in (-3, 0, 3) for b in (-3, 0, 3))]
            if near:
                cx = sum(x for x, _ in near) // len(near); cy = sum(y for _, y in near) // len(near)
                ball = mat.keep(f, mat.region(f.size, [[(cx - 4, cy - 4), (cx + 4, cy - 4), (cx + 4, cy + 4), (cx - 4, cy + 4)]]))
                ball = mat.keep(ball, mat.mask_not(mat.colour_mask(ball, [H('b9b9db'), H('d0c8c0')])))
                g = mat.paste(g, ball, 0, 0)
        out.append(mat.drop_specks(mat.clean_orphans(g), 25))
        print('frame', i, 'head offset', dx, dy)
    return out


BAG_B = {0: (-30, 2), 1: (-28, 2), 2: (-28, 2), 3: (-30, -2), 4: (-44, -10)}


def strip(frames, k=2):
    w, h = frames[0].size
    s = Image.new('RGBA', (w * len(frames), h), CLEAR)
    for i, f in enumerate(frames):
        s.paste(f, (i * w, 0))
    return kb.up(s, k)


if __name__ == '__main__':
    key = (sys.argv[1:] or ['A'])[0]
    frs = {'A': back_a, 'B': back_b}[key]()
    st = strip(frs, 1)
    st.save(kb.WORK + '/passes/plb_%s_native.png' % key)
    kb.up(kb.on_bg(st, (150, 160, 170, 255)), 3).save('/tmp/plb_%s.png' % key)
