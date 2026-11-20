"""Captain Edda Morrow battle fronts (80-px art, 160x160 export). python3 -I tools/kitbash/edda.py [variant ...]
Concept: the ferry captain who smuggled a child out on the night ferry and brought them back on the last one. Squat, round,
weathered, gruff; navy + rust red; a red knit watch cap on a barrel; gold tooth; Lapras tattoo on a bare forearm.
  A body : sd sailor (BW Sailor class: barrel body, binoculars at the chest)  -> navy pea coat, brass buttons, red neckerchief
  head   : the Sailor's own, re-made: cap -> ribbed red watch cap, grey curls out from under it, gold-tooth grin, crow's feet
  B body : sd sailor-gen6 (flexing)                                            -> showing off the Lapras tattoo
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'EDDA', '21_edda.png'
TITLE = ('CAPTAIN EDDA MORROW - 64, the ferry Dovetail. Battle front kitbash (80-px art, file 160x160). Concept: a squat navy barrel '
         'under a red watch cap; gold tooth, Lapras tattoo, binoculars. Gruff with a hidden tenderness.')


def sd(n):
    return show.get_native('sd:' + n)[0]


X = {'k': BLACK, 'r': H('c0402e'), 'R': H('8a2a1e'), 'q': H('e0604a'), 'g': H('b8b8c4'), 'G': H('8a8a98'), 'w': H('ffffff'),
     'y': H('f0c040'), 'Y': H('b08820'), 'b': H('3a78c0'), 'B': H('7ab0e8'), 's': H('ffd5bd'), 'S': H('dea47b'), 'm': H('bd7b62'),
     'n': H('7b4a5a')}
NAVY = {H('ffffff'): H('3e5c8c'), H('c5c5e6'): H('2c4470'), H('7b7b9c'): H('1e2c4c'), H('6a7bac'): H('2c4470'),
        H('4a5a83'): H('1e2c4c'), H('293952'): H('141c30')}
TROUSER = {H('ffffff'): H('4a4e5c'), H('c5c5e6'): H('3a3e4a'), H('7b7b9c'): H('262832'), H('6a7bac'): H('3a3e4a'),
           H('4a5a83'): H('262832'), H('293952'): H('1a1c24')}
BINO = {H('293952'): H('1a1a1e'), H('4a5a83'): H('34343c'), H('6a7bac'): H('b08820'), H('c5c5e6'): H('f0c040'),
        H('7b7b9c'): H('5a5a64'), H('ffffff'): H('e8e8f0')}


def watch_cap(im, box):
    p = im.load(); x0, y0, x1, y1 = box
    cap = set(H(c) for c in ('c5c5e6', 'ffffff', '6a7bac', '4a5a83', '7b7b9c'))
    for y in range(y0, y1):
        for x in range(x0, x1):
            if p[x, y] in cap:
                if y >= y1 - 2:
                    p[x, y] = X['R'] if x % 2 else X['r']          # folded cuff
                elif y == y0 + 1:
                    p[x, y] = X['q']                                # light on the crown
                else:
                    p[x, y] = X['r'] if x % 2 else X['R']           # knit ribs
    return im


def build(var='A'):
    if var == 'B':
        return build_b()
    s = sd('sailor')
    head = mat.region(s.size, rect=(30, 0, 56, 24))
    bino = mat.region(s.size, rect=(20, 24, 42, 36))
    legs = mat.region(s.size, rect=(0, 55, 80, 80))
    s = mat.recolour(s, BINO, bino)
    s = mat.recolour(s, TROUSER, mat.mask_and(legs, mat.mask_not(bino)))
    s = mat.recolour(s, NAVY, mat.mask_not(mat.mask_or(mat.mask_or(head, bino), legs)))
    s = watch_cap(s, (32, 6, 52, 15))
    # grey curls out from under the cap (the Sailor's dark hair goes grey), and on the far side too
    s = mat.recolour(s, {H('293952'): X['G'], H('4a5a83'): X['g']}, mat.region(s.size, rect=(44, 11, 54, 18)))
    s = mat.patch(s, 32, 13, ['.gk', 'gGk', 'kgk', '.k.'], X)
    # face: grey brows, crow's feet, gold-tooth grin
    s = mat.patch(s, 35, 15, ['GG.....GG'], X)
    s = mat.patch(s, 34, 18, ['m'], X); s = mat.patch(s, 48, 18, ['m'], X)
    s = mat.patch(s, 39, 21, ['k....k', '.kwywk', '..kkk.'], X)
    # chest: the emblem goes, brass buttons in two rows, red neckerchief knot
    p = s.load()
    for y in range(36, 48):
        for x in range(30, 42):
            if p[x, y][3] and p[x, y] not in (BLACK,) and p[x, y] not in NAVY.values():
                p[x, y] = NAVY[H('c5c5e6')]
    for (x, y) in [(33, 39), (39, 39), (33, 44), (39, 44), (33, 49), (39, 49)]:
        s = mat.patch(s, x, y, ['y', 'Y'], X)
    s = mat.patch(s, 41, 24, ['.rr.', 'rqrR', '.RR.', 'r..R'], X)
    # Lapras tattoo on the bare right forearm
    s = mat.patch(s, 51, 30, ['.b..', 'bBb.', '.bbb'], X)
    return s


def build_b():
    s = sd('sailor-gen6')
    return s


VARIANTS = [('A', 'A: the Dovetail. A navy barrel with brass buttons under a ribbed red watch cap, grey curls poking out, gold-tooth '
                  'grin, binoculars ready, a Lapras tattoo on the bare forearm. Sailor class body and head, re-made.')]
PICK = 'A'
REFS = [('sd:sailor', 'Sailor (official BW)'), ('sd:clay', 'Clay (official BW)'), ('sd:bertha', 'Bertha (official)'),
        ('reborn:093', 'Reborn front (Julia)')]
DONORS = [('sd:sailor', 'sailor: body, binoculars, head (re-made)')]
NOTE = 'Hand pixels: ribbed cap texture, grey curls, brows, crow\'s feet, gold-tooth grin, brass buttons, neckerchief, Lapras tattoo.'

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/edd_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/edd.png')
