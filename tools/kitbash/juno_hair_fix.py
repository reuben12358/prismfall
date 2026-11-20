"""Juno pass-3 portraits: HAIR FIX only. Face, eyes, mouths, freckles, wreath, big bloom and veil are untouched.
The old hair (Rosa's hat repainted + Hilda's mass) read choppy: stair-stepped outline, black strand lines, flat bands.
Here the hair pixels are found (3 hair colours + the black lines inside the hair), the outer silhouette is smoothed, and the
mass is re-shaded as a few wavy locks flowing from the crown: 4 shades + one highlight band, clusters not stripes.
python3 -I tools/kitbash/juno_hair_fix.py
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, CLEAR, BLACK
from PIL import Image, ImageFilter

P, J = kb.WORK + '/passes', kb.WORK + '/juno'
EXPR = ['happy', 'surprised', 'sad', 'neutral']
HAIR_OLD = {H('963a24'), H('c8582e'), H('5a2018')}
# shades, dark -> light; the two middle ones are pass 3's own hair colours, so the look stays B2W2-bright
SH = [H('6a2219'), H('963a24'), H('c8582e'), H('e07a40')]
HI = H('f5a066')
LINE = BLACK          # outer outline: very dark auburn instead of pure black, softer like the B2W2 busts' hair

CROWN = (25.0, -7.0)
LOCKS = 9.5
BAND_W = 1.3
BAND_R = 18.5
BAND_SOLID = False
LOCK_AMP = 0.27        # the part sits above the frame; locks radiate from here


def classify(im):
    """-> set of hair pixels (incl. internal black strand lines), set of outer-outline blacks to rebuild."""
    p = im.load(); hair = set(); outer = set()
    for y in range(48):
        for x in range(48):
            if p[x, y] in HAIR_OLD:
                hair.add((x, y))
    for y in range(48):
        for x in range(48):
            if p[x, y] != BLACK:
                continue
            nb = [p[x + dx, y + dy] if 0 <= x + dx < 48 and 0 <= y + dy < 48 else CLEAR
                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            n8 = [p[x + dx, y + dy] if 0 <= x + dx < 48 and 0 <= y + dy < 48 else None
                  for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
            other = [c for c in n8 if c is not None and c[3] and c != BLACK and c not in HAIR_OLD]
            if other:
                continue                                   # face line / flower outline: keep
            if any(c[3] == 0 for c in nb):
                outer.add((x, y))
            elif sum(1 for c in n8 if c in HAIR_OLD) >= 2:
                hair.add((x, y))
    return hair, outer


def smooth_silhouette(im, hair, outer):
    """fill the stair-step notches and shave the spurs of the hair edge against empty space (never touches
    flowers, veil or face). Two passes: a notch pixel with 3+ filled 4-neighbours is filled, a hair pixel with
    only one filled 4-neighbour is cut."""
    p = im.load()
    filled = set((x, y) for y in range(48) for x in range(48) if p[x, y][3])
    region = set(hair | outer)
    for _ in range(2):
        add, rem = set(), set()
        for y in range(48):
            for x in range(48):
                n4 = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                cnt = sum(1 for q in n4 if q in filled or not (0 <= q[0] < 48 and 0 <= q[1] < 48))
                if (x, y) not in filled and cnt >= 3 and any(q in region for q in n4):
                    add.add((x, y))
                elif (x, y) in region and cnt <= 1:
                    rem.add((x, y))
        filled = (filled | add) - rem; region = (region | add) - rem
    return region


def shade(x, y, face_mask):
    cx, cy = CROWN
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    r = math.hypot(dx, dy); th = math.atan2(dx, dy)          # 0 = straight down
    # wavy locks: the strand angle drifts with distance (frizzy wave), ~7 locks across the head
    wav = th + 0.09 * math.sin(r * 0.40)
    t = (wav * LOCKS / (2 * math.pi)) % 1.0                   # 0 at a lock's lit edge -> 1 at its crease
    lock = 1.0 - 2.0 * (t ** 1.4)                             # bright lit side, falling into a dark crease
    light = -0.007 * (x - 20) - 0.008 * (y - 20)              # light from the upper left
    v = 0.55 + LOCK_AMP * lock + light
    v -= 0.10 * face_mask                                     # soft contact shadow beside the face
    rh = math.hypot(x + 0.5 - 26.0, y + 0.5 - 24.0)
    band = math.exp(-((rh - BAND_R) / BAND_W) ** 2) if y < 21 else 0.0   # highlight arc following the dome
    v += 0.30 * band * (0.6 + 0.4 * max(0.0, lock))
    return v, band


def lock_lit(x, y):
    cx, cy = CROWN
    r = math.hypot(x + 0.5 - cx, y + 0.5 - cy); th = math.atan2(x + 0.5 - cx, y + 0.5 - cy)
    t = ((th + 0.09 * math.sin(r * 0.40)) * LOCKS / (2 * math.pi)) % 1.0
    return t < 0.62                                           # the band breaks at each crease, like real sheen


def recolour_hair(im, region):
    p = im.load()
    # face proximity: pixels next to skin/face-outline get a soft contact shadow
    near = {}
    for (x, y) in region:
        d = 9
        for yy in range(y - 2, y + 3):
            for xx in range(x - 2, x + 3):
                if 0 <= xx < 48 and 0 <= yy < 48 and (xx, yy) not in region and p[xx, yy][3] and p[xx, yy] != BLACK:
                    c = p[xx, yy]
                    if c[0] > 200 and 150 < c[1] < 225 and c[2] < 200:        # skin tones
                        d = min(d, abs(xx - x) + abs(yy - y))
        near[(x, y)] = max(0.0, 1.0 - (d - 1) / 3.0) if d < 9 else 0.0
    out = im.copy(); q = out.load()
    for (x, y) in region:
        v, band = shade(x, y, near[(x, y)])
        if band > 0.5 and (BAND_SOLID or lock_lit(x, y)):
            q[x, y] = HI
            continue
        if x >= 33 and y >= 22:
            v = max(v, 0.36)                                  # no dark crease stripe down the face's right side
        k = int(round(max(0.0, min(1.0, v)) * (len(SH) - 1)))
        q[x, y] = SH[k]
    # outer outline: one clean pixel line on the new silhouette edge
    reg = set(region)
    for (x, y) in list(reg):
        edge = any(not (0 <= x + dx < 48 and 0 <= y + dy < 48) or q[x + dx, y + dy][3] == 0
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if edge and 0 < x < 47 and y > 0 and y < 47:
            q[x, y] = LINE
    return out


def cleanup(im, region):
    """single pixels of a shade surrounded by another shade -> neighbours' majority (clusters, not noise)."""
    p = im.load(); out = im.copy(); q = out.load(); allowed = set(SH) | {HI}
    for (x, y) in region:
        c = p[x, y]
        if c not in allowed:
            continue
        nb = [p[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= x + dx < 48 and 0 <= y + dy < 48 and p[x + dx, y + dy] in allowed]
        if len(nb) >= 3 and c not in nb:
            q[x, y] = max(set(nb), key=nb.count)
    return out


def fix(im):
    hair, outer = classify(im)
    region = smooth_silhouette(im, hair, outer)
    out = im.copy(); op = out.load()
    for (x, y) in outer | hair:
        if (x, y) not in region:
            op[x, y] = CLEAR
    out = recolour_hair(out, region)
    return cleanup(cleanup(out, region), region)


def main():
    for e in EXPR:
        im = Image.open(P + '/p3_A_%s_48.png' % e).convert('RGBA')
        f = fix(im)
        f.save(P + '/p3h_%s_48.png' % e)
        kb.up(f, 2).save(J + '/JUNO_%s_p3h.png' % e)
    print('ok')


if __name__ == '__main__' and sys.argv[1:2] != ['middle']:
    main()


# ---------------------------------------------------------------- middle ground (pass 3 structure + fix shading)
DARK = H('4e1a14')          # inner lock contour: two shades under the hair's darkest, never black


def contours(orig, region):
    """pass 3's internal black strand lines, kept only where they are real lock divisions (runs of 4+ px), tapered by
    trimming each run's free ends."""
    hair, outer = classify(orig)
    p = orig.load()
    lines = set(q for q in hair if p[q] == BLACK) & region
    comps, seen = [], set()
    for q in lines:
        if q in seen:
            continue
        st, comp = [q], []
        while st:
            c = st.pop()
            if c in seen or c not in lines:
                continue
            seen.add(c); comp.append(c)
            st += [(c[0] + dx, c[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
        comps.append(comp)
    keep = set()
    for comp in comps:
        if len(comp) < 4:
            continue
        cs = set(comp)
        ends = [c for c in comp if sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                                       if (dx or dy) and (c[0] + dx, c[1] + dy) in cs) <= 1]
        keep |= cs - set(ends)
    return keep


def middle(e):
    orig = Image.open(P + '/p3_A_%s_48.png' % e).convert('RGBA')
    hair, outer = classify(orig)
    region = smooth_silhouette(orig, hair, outer)
    out = fix(orig)
    q = out.load(); po = orig.load()
    # the dark band the wreath sits on (pass 3's darkest hair tone) comes back as the darkest shade
    for (x, y) in region:
        if po[x, y] == H('5a2018') and q[x, y] in set(SH) | {HI}:
            q[x, y] = SH[0]
    for (x, y) in contours(orig, region):
        if q[x, y] in set(SH) | {HI}:
            q[x, y] = DARK
    return out


def main_middle():
    global BAND_W, LOCK_AMP, BAND_R, BAND_SOLID
    BAND_W, LOCK_AMP, BAND_R, BAND_SOLID = 0.75, 0.22, 21.5, True   # one crisp band over the crown, above the wreath
    for e in EXPR:
        m = middle(e)
        m.save(P + '/p3m_%s_48.png' % e)
        kb.up(m, 2).save(J + '/JUNO_%s_p3m.png' % e)
    print('middle ok')


if __name__ == '__main__' and sys.argv[1:2] == ['middle']:
    main_middle()
