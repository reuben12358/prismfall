"""Juno portrait refresh (style test only, nothing installed). Keeps pass 3 exactly (face, eyes, hair, wreath,
bloom); changes only the veil strip on the right edge, per STYLE_GUIDE 4.8 (translucent layers):
- the grey specks (#807175) in the veil are removed (they read as dirt);
- the hard vertical inner edge becomes a hem that steps 1 px in and out (it flutters instead of reading as a panel);
- one soft pleat (shadow line + light line) runs down the veil.
python3 -I art/research/scripts/juno_refresh.py [out_dir]"""
import sys, os
sys.path.insert(0, '/home/claude/fangame/tools/kitbash')
import kb
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/fangame/art/research/style_test'
SRC = '/home/claude/fangame/art/out/Graphics/Portraits/'
H = lambda s: (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)
N, Q, M, L, KK, U, J = H('ffe6ec'), H('807175'), H('e49d8c'), H('ca8e87'), H('eac0c2'), H('f4c6c4'), H('fff8f0')
VEIL = {N, Q, M, L, KK, U}
PLEAT_D = {M: H('d48a86'), L: H('b47a7c'), N: KK}       # one step darker inside each zone
PLEAT_L = {M: U, L: H('dca29c'), N: J}


def refresh(im):
    im = im.copy(); p = im.load()
    for y in range(6, 48):                                  # 1. specks -> the zone colour around them
        for x in range(40, 48):
            if p[x, y] == Q:
                nb = [p[xx, y] for xx in (x - 1, x + 1) if 0 <= xx < 48 and p[xx, y] in VEIL - {Q}]
                nb += [p[x, yy] for yy in (y - 1, y + 1) if 0 <= yy < 48 and p[x, yy] in VEIL - {Q}]
                p[x, y] = nb[0] if nb else (KK if y < 21 else (M if y < 30 else L))
    for y in range(21, 48):                                 # 2. fluttering hem: in at 43 for alternate 6-row blocks
        zone = M if y < 30 else L
        if (y - 21) // 6 % 2 == 1 and p[42, y] in (U, KK):
            p[42, y] = p[41, y]                             # hair shows where the hem steps in
            p[43, y] = U if y < 30 else KK
        elif p[42, y] in (U, KK) and p[43, y] == zone:
            pass
    for y in range(22, 48):                                 # 3. one pleat, drifting right as it falls
        x = 44 + (y - 22) // 9
        if x + 1 < 48 and p[x, y] in PLEAT_D and p[x + 1, y] in PLEAT_L:
            p[x, y] = PLEAT_D[p[x, y]]; p[x + 1, y] = PLEAT_L[p[x + 1, y]]
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for e in ('', '_happy'):
        src = kb.native(kb.load(SRC + 'JUNO%s.png' % e))[0]
        r = refresh(src)
        diff = sum(1 for y in range(48) for x in range(48) if src.getpixel((x, y)) != r.getpixel((x, y)))
        outside = sum(1 for y in range(48) for x in range(40) if src.getpixel((x, y)) != r.getpixel((x, y)))
        r.save(OUT + '/JUNO%s_refresh_48.png' % e); r.resize((96, 96), Image.NEAREST).save(OUT + '/JUNO%s_refresh.png' % e)
        print('JUNO%s: %d px changed, %d of them left of x=40 (must be 0)' % (e, diff, outside))
