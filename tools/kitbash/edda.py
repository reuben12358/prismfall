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
TITLE = ('CAPTAIN EDDA MORROW, pass 2 - 64, the ferry Dovetail. Battle front kitbash (80-px art, file 160x160). Concept: a squat navy barrel '
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


# ---------------------------------------------------------------- pass 2: the night ferry (Hiker class body, rebuilt)
HIKE = {H('c0a878'): H('2c4470'), H('887860'): H('1e2c4c'), H('e8d078'): H('3e5c8c'),     # vest -> navy pea coat
        H('e87050'): H('2c4470'), H('a85040'): H('1e2c4c'), H('784858'): H('141c30'),     # sleeves -> navy
        H('286050'): H('141c30'), H('387060'): H('1e2c4c')}
ROPE = {H('e8d078'): H('d8c090'), H('c0a878'): H('b09060'), H('887860'): H('7a6040'), H('a87860'): H('5a4630')}
SKIN = H('f8d0b8'); SKIN2 = H('d8a078'); SKIN3 = H('a87860')


def lantern(im, x, y):
    L = dict(X); L.update({'o': H('5a4a2a'), 'O': H('b08820'), 'l': H('fff2b0'), 'L': H('ffd060'), 'f': H('f08a30'),
                           'h': H('fff8d8')})
    im = mat.patch(im, x - 2, y - 2, ['..hh.hh..', '.h.....h.', 'h.......h'], L)          # a little glow
    return mat.patch(im, x, y, ['..kkk..',
                                '.k...k.',
                                '.kOOOk.',
                                'kOkkkOk',
                                'kOlLlOk',
                                'kOLfLOk',
                                'kOlLlOk',
                                'kOkkkOk',
                                '.kOOOk.',
                                '..kkk..'], L)


def night_ferry():
    b = sd('hiker')
    p = b.load()
    rope_r = mat.region(b.size, [[(48, 12), (68, 12), (68, 38), (50, 38)]])
    pack_r = mat.region(b.size, [[(50, 24), (60, 24), (60, 50), (50, 50)]])
    b = mat.recolour(b, ROPE, rope_r)
    b = mat.recolour(b, {H('286050'): H('5a4630'), H('387060'): H('7a6040')}, pack_r)       # rucksack -> rope strap / satchel
    head_r = mat.region(b.size, rect=(24, 2, 50, 28))
    b = mat.recolour(b, HIKE, mat.mask_and(mat.mask_not(head_r), mat.mask_not(rope_r)))
    b = mat.recolour(b, {H('e87050'): H('2c4470'), H('a85040'): H('1e2c4c')}, mat.region(b.size, rect=(0, 22, 80, 62)))
    # trousers stay dark; boots -> black sea boots; stick -> boat hook (wood + brass)
    b = mat.recolour(b, {H('e87050'): H('2a2a30'), H('a85040'): H('1a1a20')}, mat.region(b.size, rect=(0, 62, 80, 80)))
    b = mat.recolour(b, {H('e8e8f8'): H('a07040'), H('f8f8f8'): H('a07040'), H('c0c0d0'): H('7a5030')},
                     mat.region(b.size, rect=(44, 46, 54, 80)))
    p = b.load()
    # face: beard out, a weathered round face with a jaw line
    beard = (H('483830'), H('382828'), H('605050'))
    face_r = mat.region(b.size, rect=(31, 16, 50, 28)).load()
    for y in range(16, 28):
        for x in range(31, 50):
            if face_r[x, y] and p[x, y] in beard:
                p[x, y] = SKIN2 if (y >= 23 or x >= 45) else SKIN
    for y in range(18, 28):
        for x in range(31, 50):
            if p[x, y] in (SKIN, SKIN2) and any(p[x + dx, y + dy][3] == 0 or p[x + dx, y + dy] not in (SKIN, SKIN2, SKIN3, BLACK,
                    H('e8e8f8'), H('f8f8f8'), H('a85040'), H('e87050'), H('d8a078'), H('a87860'))
                    for dx, dy in ((0, 1), (1, 0), (-1, 0)) if 0 <= x + dx < 80 and y + dy < 80) and y >= 24:
                p[x, y] = BLACK
    # hat -> ribbed red watch cap (brim trimmed to the head)
    for y in range(3, 15):
        for x in range(24, 52):
            c = p[x, y]
            if c in (H('c0a878'), H('887860'), H('e87050'), H('a85040'), H('e8d078')):
                if y >= 12 and (x < 32 or x > 47):
                    p[x, y] = CLEAR
                elif y >= 11:
                    p[x, y] = X['R'] if x % 2 else X['r']
                elif y <= 5:
                    p[x, y] = X['q']
                else:
                    p[x, y] = X['r'] if x % 2 else X['R']
    b = mat.clean_orphans(b)
    b = mat.recolour(b, {H('e8d078'): X['g'], H('c0a878'): X['G'], H('887860'): H('6a6a78')}, mat.region(b.size, rect=(24, 13, 34, 25)))
    b = mat.recolour(b, HIKE, mat.region(b.size, rect=(24, 23, 50, 30)))
    p = b.load()
    # grey curls under the cap, both sides; gold-tooth grin with a rose lip; brows softened
    b = mat.patch(b, 28, 12, ['..kgg', '.kgGg', 'kgGgg', 'kggG.', 'kGgg.', '.kgG.', 'kggk.', '.kk..'], X)
    b = mat.patch(b, 46, 12, ['gg..', 'gGk.', 'gGgk', '.gGk', 'gGgk', '.ggk', '.kk.'], X)
    b = mat.patch(b, 36, 20, ['n.....n', '.kwwywk', '..nnnn.'], dict(X, n=H('c06070')))
    b = mat.patch(b, 37, 14, ['GG...GG'], X)
    b = mat.patch(b, 33, 18, ['pp.......pp'], dict(X, p=H('f0a0a0')))            # rosy, windburnt cheeks
    b = mat.patch(b, 34, 16, ['k'], X); b = mat.patch(b, 45, 16, ['k'], X)          # lashes at the outer corners
    # the storm lantern held high in the waving hand; the tattoo peeks from the rolled cuff
    b = lantern(b, 6, 14)
    b = mat.patch(b, 17, 26, ['.b.', 'bBb', 'bb.'], X)
    # knee-length pea coat: the trousers' upper half becomes the coat skirt (their folds kept), and a flap flares out
    # behind her in the wind
    b = mat.recolour(b, {H('483830'): H('2c4470'), H('382828'): H('1e2c4c'), H('605050'): H('3e5c8c')},
                     mat.region(b.size, rect=(14, 46, 50, 60)))
    flap = Image.new('RGBA', (80, 80), CLEAR)
    reg = mat.region((80, 80), [[(22, 50), (24, 60), (16, 66), (10, 64), (16, 56)]]).load()
    fp = flap.load()
    for y in range(80):
        for x in range(80):
            if reg[x, y]:
                fp[x, y] = H('1e2c4c') if (x - y) % 5 else H('2c4470')
    flap = mat.outline_outer(flap, BLACK)
    b = mat.under(b, flap, 0, 0)
    for (x, y) in [(31, 34), (37, 34), (31, 40), (37, 40), (31, 50), (37, 50)]:
        b = mat.patch(b, x, y, ['y', 'Y'], X)
    b = mat.patch(b, 36, 27, ['rqrr', 'RrrR', '.rR.'], X)                          # red neckerchief
    return b


def build(var='A'):
    if var == 'N':
        return night_ferry()
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
    # grey curls hanging from under the cap to the jaw (outer edge outlined, inner edge merging into the face)
    s = mat.patch(s, 31, 13, ['.kkgg', 'kgGg.', 'kggG.', 'kGgg.', '.kgG.', 'kgGg.', 'kggk.', '.kGg.', '..kk.'], X)
    s = mat.patch(s, 48, 13, ['ggkk.', '.gGgk', '.Gggk', '.ggGk', '.Ggk.', '.gGgk', '.kggk', '.gGk.', '.kk..'], X)
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
    s = mat.patch(s, 42, 25, ['rrqr', 'RrrR', '.qR.', 'r..R'], X)
    # Lapras tattoo on the bare right forearm
    s = mat.patch(s, 51, 30, ['.b..', 'bBb.', '.bbb'], X)
    return s


NAVY6 = {H('ffffff'): H('3e5c8c'), H('9fb5d1'): H('2c4470'), H('59738d'): H('1e2c4c'), H('253651'): H('141c30'),
         H('4f9ad3'): H('c0402e'), H('39729c'): H('8a2a1e'), H('c5bbba'): H('2c4470')}
TROUSER6 = {H('ffffff'): H('4a4e5c'), H('9fb5d1'): H('3a3e4a'), H('59738d'): H('262832'), H('253651'): H('1a1c24')}


def build_b():
    s = sd('sailor-gen6')
    cap = mat.region(s.size, rect=(26, 6, 48, 15))
    p = s.load()
    for y in range(6, 15):
        for x in range(26, 48):
            if p[x, y] in (H('ffffff'), H('9fb5d1'), H('4f9ad3'), H('39729c'), H('59738d'), H('253651')):
                p[x, y] = X['r'] if y > 8 else X['q']
    for y in range(9, 14):
        for x in range(26, 48):
            if p[x, y] in (X['r'],):
                p[x, y] = X['r'] if x % 2 else X['R']           # knit ribs
    for x in range(26, 48):
        if p[x, 13] in (X['r'], X['R']):
            p[x, 13] = X['R']
    s = mat.recolour(s, TROUSER6, mat.region(s.size, rect=(0, 48, 80, 80)))
    s = mat.recolour(s, NAVY6, mat.mask_not(mat.mask_or(cap, mat.region(s.size, rect=(0, 48, 80, 80)))))
    s = mat.patch(s, 25, 13, ['..kk..', '.kggk.', 'kgGgk.', 'kggGk.', '.kGgk.', 'kgggk.', '.kgk..', '..k...'], X)
    s = mat.patch(s, 42, 13, ['.kk..', 'kggk.', 'kgGgk', '.kggk', 'kgGk.', '.kgk.', '..k..'], X)
    s = mat.patch(s, 33, 22, ['k....k', '.kwywk', '..kkk.'], X)
    s = mat.patch(s, 47, 22, ['..b..', '.bBb.', 'bbbb.', '.b.b.'], X)       # the Lapras tattoo on the flexed arm
    return s


VARIANTS = [('N', 'N (pass 2): the night ferry. Storm lantern held high in a waving hand ("Don\'t look down at the strait at '
                  'night, sprog"), a coil of rope over her shoulder, a boat hook for a stick; navy pea coat to the knee with brass '
                  'buttons, its tail flaring in the wind; red watch cap, grey curls, rosy windburnt cheeks, gold-tooth grin, '
                  'Lapras tattoo at the cuff. Hiker class body (beard out, face rebuilt).'),
            ('A', 'A (pass 1): the Dovetail. A navy barrel with brass buttons under a ribbed red watch cap, grey curls poking out, gold-tooth '
                  'grin, binoculars ready, a Lapras tattoo on the bare forearm. Sailor class body and head, re-made.'),
            ('B', 'B: "Tide\'s got a sense of humour." Double-arm flex to show off the Lapras tattoo, navy coat, red cap and '
                  'neckerchief, gold-tooth grin. Sailor (gen 6 style) body, same treatment.')]
PICK = 'N'
REFS = [('sd:hiker', 'Hiker (official BW)'), ('sd:sailor', 'Sailor (official BW)'), ('sd:clay', 'Clay (official BW)'), ('sd:bertha', 'Bertha (official)'),
        ('reborn:093', 'Reborn front (Julia)')]
DONORS = [('sd:hiker', 'hiker: N body, waving arm, bedroll -> rope coil, stick -> boat hook, face rebuilt'),
          ('sd:sailor', 'sailor: A body, binoculars, head (re-made)'), ('sd:sailor-gen6', 'sailor-gen6: B body (flex)')]
NOTE = 'Hand pixels (N): storm lantern + glow, coat flap, beard repainted to skin, cheeks, lashes. (A/B): ribbed cap texture, grey curls, brows, crow\'s feet, gold-tooth grin, brass buttons, neckerchief, Lapras tattoo.'

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/edd_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/edd.png')
