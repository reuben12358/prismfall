"""player2_ow.py - PLAYER_A / PLAYER_B overworld walk sheets: 128x192, 4 frames x 4 directions (down, left, right, up),
32x48 frames = 16x24 art doubled, the layout of art/out/Graphics/Characters/JUNO.png (cols: stand, step, stand, step;
step frames sit 1 px lower, as Juno's do). Hand-placed pixels: one head per facing, legs per step. Right = mirror of left.
python3 -I art/research/scripts/player2_ow.py [A|B] [scheme]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p2kit import hx, up, mirror
import player2_palette as P
from PIL import Image

OUT = '/home/claude/fangame/art/work/redo_v2/'


def legend(sc, ch):
    h, T, C, S, Y = sc['hair'], sc['teal'], sc['cream'], sc['slate'], sc['yel']
    boot = h if ch == 'A' else (S[0], S[1], S[2], S[3], S[3])
    return {'K': P.K, 'o': P.K,
            't': T[0], 'T': T[1], 'u': T[2], 'U': T[3],
            'c': C[0], 'C': C[1], 'v': C[2], 'V': C[3],
            'z': S[1], 'Z': S[2], 'x': S[3],
            'H': h[0], 'n': h[1], 'N': h[2], 'm': h[3],
            's': P.SKIN[1], 'S': P.SKIN[2], 'e': sc['iris'][1],
            'b': boot[2], 'B': boot[3], 'Y': Y[1], 'y': Y[2]}


def render(rows, L):
    im = Image.new('RGBA', (16, 24), (0, 0, 0, 0)); p = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in '. ': continue
            p[x, y] = hx(L[ch])
    return im


# ------------------------------------------------------------------------------------------- PLAYER_A
# A facing = head (15 rows, 0..14) + torso (4 rows) + legs (4 rows) + a blank row = 24. Content sits on rows 3..22 like Juno's.
# A step frame is the whole figure 1 px lower (rows 4..23, as Juno's) with the stepping legs.
A = {
 'down': {
  'head': ['................',
           '................',
           '................',
           '.....KKKKKK.....',
           '...KTTttTTTuK...',
           '...KccccccccK...',
           '.KKKTTTTTTTTKKK.',
           'KtTTTTTTTTTTTTuK',
           'KKKnNNNNNNNNnKKK',
           '..KNnNsNNsNnNK..',
           '..KNsssssssssK..',
           '..KsKssssssKsK..',
           '..KsessssssesK..',
           '...KsssSSssSK...',
           '....KKssssKK....'],
  'torso': ['...KCCKzzKCCKKK.',
            '..KCCCKzzKCCKTuK',
            '..KsCCKzzKCvKTuK',
            '..KsKCCzzCCKsKUK'],
  'legs': ['...KKzzzzzzKKK..',
           '....KzzKKzzK....',
           '....KbbK.KbbK...',
           '....KKK..KKK....'],
  'step1': ['...KKzzzzzzKKK..',
            '....KzzKKbbK....',
            '....KbbK.KKK....',
            '....KKK.........'],
  'step2': ['...KKzzzzzzKKK..',
            '....KbbKKzzK....',
            '....KKK.KbbK....',
            '.........KKK....'],
 },
 'left': {
  'head': ['................',
           '................',
           '................',
           '.....KKKKKK.....',
           '...KTTttTTTuK...',
           '...KccccccccK...',
           '.KKKTTTTTTTTKKK.',
           'KtTTTTTTTTTTTTuK',
           'KKKnNNNNNNNmKKK.',
           '..KNnNNNNNNmmK..',
           '..KsNNsNNNNmmK..',
           '.KssKssSNNNmK...',
           '.KsseSssSSmmK...',
           '..KsssSSSmmK....',
           '...KKssssKK.....'],
  'torso': ['....KCCzzCCKK...',
            '...KCCCzKCCTuK..',
            '...KCCsKCCvKTuK.',
            '...KCssKCCKKTUK.'],
  'legs': ['....KKzzzzKKKK..',
           '.....KzzzzK.....',
           '.....KbbbbK.....',
           '.....KKKKKK.....'],
  'step1': ['....KKzzzzKKKK..',
            '...KzzKKKzzK....',
            '..KbbK...KbbK...',
            '..KKK....KKK....'],
  'step2': ['....KKzzzzKKKK..',
            '....KzzKzzK.....',
            '...KbbKKbbK.....',
            '...KKK.KKK......'],
 },
 'up': {
  'head': ['................',
           '................',
           '................',
           '.....KKKKKK.....',
           '...KTTttTTTuK...',
           '...KccccccccK...',
           '.KKKTTTTTTTTKKK.',
           'KtTTTTTTTTTTTTuK',
           'KKKnNNNNNNNNmKKK',
           '..KNnNNNNNNNmK..',
           '..KNNnNNNNNmmK..',
           '..KmNNNNNNNmmK..',
           '..KsmNNNNNmmsK..',
           '...KmmNNNmmmK...',
           '....KKKKKKKK....'],
  'torso': ['..KKCCCCCCCKK...',
            '.KTuKCCCCCCCK...',
            '.KTuKCCCCCvsK...',
            '.KUTKCCCCCvsK...'],
  'legs': ['...KKzzzzzzKK...',
           '....KzzKKzzK....',
           '....KbbK.KbbK...',
           '....KKK..KKK....'],
  'step1': ['...KKzzzzzzKK...',
            '....KzzKKbbK....',
            '....KbbK.KKK....',
            '....KKK.........'],
  'step2': ['...KKzzzzzzKK...',
            '....KbbKKzzK....',
            '....KKK.KbbK....',
            '.........KKK....'],
 },
}

# PLAYER_B: the side tail hangs on her right (screen left facing down, behind her facing left, screen right facing up);
# the teal bow sits at its root. Bare legs, cream knee socks, slate boots, the bag at her left hip.
B = {
 'down': {
  'head': ['................',
           '................',
           '.KK.KK..........',
           'KtTKTtKKKKKKK...',
           'KTuKuKnnNNNNNKK.',
           '.KKnKNNNNNNNNNNK',
           'KnKKNnNNNNNNNnNK',
           'KnKNNNNNNNNNNNNK',
           'KNKNNNsNNNNsNNNK',
           'KNKNsssssssssNK.',
           'KmKKssKssssKsNK.',
           'KmK.ssessssesK..',
           'KmK.KssSSssSK...',
           'KmK..KKssssKK...',
           '.KmKKCCKzzKCCK..'],
  'torso': ['..KKCCCuKzKCCCK.',
            '...KsCCCuzKCCsK.',
            '...KsKCCzuzCKsKK',
            '....KKzzzzuzKKTK'],
  'legs': ['....KzzzzzzzKTuK',
           '....KssK.KssK.K.',
           '....KccK.KccK...',
           '....KbbK.KbbK...'],
  'step1': ['....KzzzzzzzKTuK',
            '....KssKKccK..K.',
            '....KccKKbbK....',
            '....KbbK.KKK....'],
  'step2': ['....KzzzzzzzKTuK',
            '....KccKKssK..K.',
            '....KbbKKccK....',
            '....KKK.KbbK....'],
 },
 'left': {
  'head': ['................',
           '................',
           '.......KK.KK....',
           '......KTtKtTK...',
           '.....KKKuKuTKK..',
           '....KnNNNNKKnNK.',
           '...KnNNNNNNNNnNK',
           '..KnNNNNNNNNNNNK',
           '..KsNNNNNNNNNNmK',
           '..KsssNNNNNNNmKK',
           '..KKssssNNNmKmNK',
           '..KesssssSNmKmNK',
           '...KssSSSsKKKmNK',
           '....KKssKK..KmK.',
           '.....KCCzzCCKmK.'],
  'torso': ['....KCCCzzCCKK..',
            '...KCCsKCCCKK...',
            '...KCssKCCCK....',
            '....KzzzzzzKK...'],
  'legs': ['.....KzzzzzKuK..',
           '.....KssssK.....',
           '.....KccccK.....',
           '.....KbbbbK.....'],
  'step1': ['....KzzzzzzKuK..',
            '...KssKKKccK....',
            '..KccK...KbbK...',
            '..KbbK...KKK....'],
  'step2': ['....KzzzzzzKuK..',
            '....KssKccK.....',
            '...KccKKbbK.....',
            '...KbbK.KKK.....'],
 },
 'up': {
  'head': ['................',
           '................',
           '..........KK.KK.',
           '...KKKKKKKtTKTtK',
           '..KKnNNNNnKuKuTK',
           '.KnNNNNNNNNKnKK.',
           '.KnNNNNNNNNNKnK.',
           '.KNNnNNNNNNNKNNK',
           '.KNNNNNNNNNNKNNK',
           '.KNNNNNNNNNmKNmK',
           '.KmNNNNNNNmmKNmK',
           '.KsmNNNNNmmsKmmK',
           '..KsmmNmmmsKKmmK',
           '...KKsssssKK.KmK',
           '..KKCCCCCCCKK.K.'],
  'torso': ['.KCCCzzCCCCCCK..',
            '.KsCCCzzCCCCsK..',
            '.KsCCCCCzzCvsK..',
            '.KKKzzzzzzzzKK..'],
  'legs': ['.KuTKzzzzzzzK...',
           '..K.KssK.KssK...',
           '....KccK.KccK...',
           '....KbbK.KbbK...'],
  'step1': ['.KuTKzzzzzzzK...',
            '..K.KssKKccK....',
            '....KccKKbbK....',
            '....KbbK.KKK....'],
  'step2': ['.KuTKzzzzzzzK...',
            '..K.KccKKssK....',
            '....KbbKKccK....',
            '....KKK.KbbK....'],
 },
}


def frames(table, L):
    """-> {direction: [stand, step1, stand, step2]} 16x24 images; right = mirror of left."""
    out = {}
    for d, p in table.items():
        stand = render(p['head'] + p['torso'] + p['legs'] + ['.' * 16], L)
        s1 = render(['.' * 16] + p['head'] + p['torso'] + p['step1'], L)
        s2 = render(['.' * 16] + p['head'] + p['torso'] + p['step2'], L)
        out[d] = [stand, s1, stand, s2]
    out['right'] = [mirror(f) for f in out['left']]
    return out


def sheet(ch, scheme='main'):
    sc = P.SCHEMES[ch][scheme]; L = legend(sc, ch)
    fr = frames(A if ch == 'A' else B, L)
    out = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
    for r, d in enumerate(('down', 'left', 'right', 'up')):
        for c_, f in enumerate(fr[d]):
            out.alpha_composite(f, (c_ * 16, r * 24))
    return out


if __name__ == '__main__':
    ch = sys.argv[1] if len(sys.argv) > 1 else 'A'
    scheme = sys.argv[2] if len(sys.argv) > 2 else 'main'
    d = OUT + 'PLAYER_%s/' % ch; os.makedirs(d, exist_ok=True)
    s = sheet(ch, scheme); suf = '' if scheme == 'main' else '_' + scheme
    s.save(d + 'PLAYER_%s_ow%s_native.png' % (ch, suf)); up(s, 2).save(d + 'PLAYER_%s_ow%s.png' % (ch, suf))
    print('ok', up(s, 2).size)
