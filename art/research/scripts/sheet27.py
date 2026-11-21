"""Sheet 27: style test of art/STYLE_GUIDE.md on Juno (refresh) and Dorian Pell (new, original construction).
silhouette row -> chosen design -> 96x96 portrait. Nothing is installed.
python3 -I art/research/scripts/sheet27.py"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/fangame/tools/kitbash')
import kb
import dorian_portrait as dp
import juno_refresh as jr
from PIL import Image, ImageDraw, ImageFont

G = '/home/claude/fangame/'
ST = G + 'art/research/style_test/'
OUT = G + 'art/previews/27_style_test.png'
F = lambda n: kb.font(n)
FB = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', n)
GAMEF = '/home/claude/ref/ebdx/Fonts/power green narrow.ttf'
BG, PANEL, INK, DIM, GOLD = (30, 30, 38, 255), (44, 44, 54, 255), (236, 236, 240, 255), (180, 180, 192, 255), (244, 208, 120, 255)
CREAM, WIN = (232, 226, 212, 255), (52, 56, 74, 255)


def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)


def plate(im, k, bg, pad=4):
    b = Image.new('RGBA', (im.width * k + pad * 2, im.height * k + pad * 2), bg)
    b.alpha_composite(up(im, k), (pad, pad)); return b


def black(im):
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); p, q = im.load(), out.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y][3]: q[x, y] = (0, 0, 0, 255)
    return out


def label(d, xy, t, f=None, fill=DIM):
    d.text(xy, t, font=f or F(12), fill=fill)


def swatches(d, x, y, groups):
    """groups: [(name, [hex...]), ...] drawn as ramps"""
    for gi, (name, cols) in enumerate(groups):
        yy = y + gi * 22
        label(d, (x, yy + 3), name, F(11), INK)
        for i, c in enumerate(cols):
            d.rectangle([x + 118 + i * 20, yy, x + 136 + i * 20, yy + 18], fill=dp.hx(c), outline=(0, 0, 0, 255))


def face_window_mock(portrait96, name, line1, line2, bgimg=None):
    W, H = 512, 384
    m = Image.new('RGBA', (W, H), (70, 90, 120, 255))
    if bgimg is not None:
        b = bgimg.copy(); b = b.crop((0, 0, min(b.width, W), min(b.height, H))); m.alpha_composite(b.convert('RGBA'))
    d = ImageDraw.Draw(m)
    # Essentials face window: 128x128 box, 96x96 face, left-aligned above the message box (Desolation layout)
    d.rectangle([8, 188, 136, 316], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=3)
    d.rectangle([16, 196, 128, 308], fill=WIN)
    m.alpha_composite(portrait96, (24, 204))
    d.rectangle([8, 320, 504, 378], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=3)
    try: gf = ImageFont.truetype(GAMEF, 24); nf = ImageFont.truetype(GAMEF, 20)
    except Exception: gf = nf = F(16)
    d.text((22, 324), line1, font=gf, fill=(72, 72, 80, 255))
    d.text((22, 349), line2, font=gf, fill=(72, 72, 80, 255))
    d.rectangle([8, 158, 8 + 14 + int(d.textlength(name, font=nf)), 184], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=2)
    d.text((15, 160), name, font=nf, fill=(56, 90, 160, 255))
    return m


def main():
    os.makedirs(ST, exist_ok=True)
    # regenerate the art
    for e in ('knowing', 'laugh', 'surprised'):
        im = dp.build(e).image(); suf = '' if e == 'knowing' else '_' + e
        im.save(ST + 'DORIAN_st%s_48.png' % suf); up(im, 2).save(ST + 'DORIAN_st%s.png' % suf)
    jsrc = kb.native(kb.load(G + 'art/out/Graphics/Portraits/JUNO.png'))[0]
    jref = jr.refresh(jsrc); jref.save(ST + 'JUNO_refresh_48.png'); up(jref, 2).save(ST + 'JUNO_refresh.png')
    jdiff = sum(1 for y in range(48) for x in range(48) if jsrc.getpixel((x, y)) != jref.getpixel((x, y)))
    dk = dp.build('knowing').image(); dl = dp.build('laugh').image(); ds = dp.build('surprised').image()

    W, H = 1900, 1716
    S = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(S)
    d.text((16, 10), 'STYLE TEST 27 - art/STYLE_GUIDE.md applied to Juno (refresh of the accepted pass 3) and Dorian Pell (new portrait, original construction)', font=FB(17), fill=INK)
    label(d, (16, 36), 'Order per guide 2.1: silhouette thumbnails -> one chosen design -> 96x96 portrait (48-px art x2). Nothing installed. Comparison point for faces_v1 (sheet 26). Recipes: art/research/scripts/{juno_refresh,dorian_portrait,sheet27}.py')

    # ---------------- JUNO ----------------
    y0 = 62
    d.rectangle([10, y0, W - 10, y0 + 560], fill=PANEL)
    d.text((22, y0 + 8), 'JUNO HALE - Ever-Bloom (Rev 12), portrait pass 3 (Rev 17) kept; refresh touches only the veil', font=FB(15), fill=GOLD)
    label(d, (22, y0 + 32), '1  Silhouettes (battle-front explorations from sheets 11-12, filled black, 1x and 2x). P3 is the installed design: wreath + veil-train + bouquet read in black.')
    names = [('A', 'eb_A'), ('B', 'eb_B'), ('C', 'eb_C'), ('P2', 'eb_P2'), ('P3 (chosen)', 'eb_P3'), ('P3 lass head', 'eb_P3_lass')]
    x = 22
    for n, f in names:
        im = kb.load(G + 'art/work/kitbash/passes/%s.png' % f)
        S.alpha_composite(plate(black(im), 2, CREAM), (x, y0 + 52))
        S.alpha_composite(plate(black(im), 1, CREAM), (x + 172, y0 + 52))
        label(d, (x, y0 + 222), n, F(12), GOLD if 'chosen' in n else DIM); x += 262
    yb = y0 + 246
    label(d, (22, yb), '2  Chosen design (installed front, 80-px art) and its colour plan: 3 colours + 1 accent (guide 2.4)')
    fr = kb.load(G + 'art/work/kitbash/juno/JUNO_everbloom_p3_native80.png')
    S.alpha_composite(plate(fr, 3, CREAM), (22, yb + 20))
    swatches(d, 280, yb + 24, [('1 ivory dress', ['fff8f0', 'f4e8dc', 'dcc6b8']), ('2 auburn hair', ['f5a066', 'c8582e', '963a24', '4e1a14']),
                               ('3 blossom pink', ['fcd2da', 'ec8aa2', 'c0506e', 'a04058']), ('accent: leaf', ['8ed07a', '48a060', '1e5a3c']),
                               ('skin', ['f8d0b8', 'd8a078', 'b08058']), ('outline', ['000000'])])
    label(d, (280, yb + 162), 'Elowen motif: leaf-green + embroidery -> green only as the accent (eyes, leaves).', F(11))
    label(d, (280, yb + 178), 'Hook in black: tilted wreath + veil train. Type colour is NOT the uniform.', F(11))
    # portrait
    xp = 800
    label(d, (xp, yb), '3  Portrait: pass 3 (installed) vs refresh. Face, eyes, hair, wreath unchanged; %d px change, all in the veil strip.' % jdiff)
    S.alpha_composite(plate(jsrc, 5, WIN), (xp, yb + 20)); label(d, (xp, yb + 270), 'pass 3, installed (5x)', F(12))
    S.alpha_composite(plate(jref, 5, WIN), (xp + 260, yb + 20)); label(d, (xp + 260, yb + 270), 'refresh (5x)', F(12), GOLD)
    for i, (im, bgc) in enumerate([(jsrc, WIN), (jref, WIN), (jsrc, CREAM), (jref, CREAM)]):
        S.alpha_composite(plate(im, 2, bgc), (xp + 530 + (i % 2) * 108, yb + 20 + (i // 2) * 108))
    label(d, (xp + 530, yb + 240), 'true size (96x96), pass 3 | refresh', F(11))
    label(d, (xp + 760, yb + 24), 'Refresh, per guide 3.8:', F(12), INK)
    for i, t in enumerate(['- grey specks (#807175) in the', '  veil removed: they read as dirt', '- one soft pleat (dark + light', '  line) so the strip reads as', '  cloth, not a flat panel', '- left of x=40: 0 px changed', '- small, reversible (Rev 17)']):
        label(d, (xp + 760, yb + 44 + i * 16), t, F(11))

    # ---------------- DORIAN ----------------
    y1 = y0 + 572
    d.rectangle([10, y1, W - 10, y1 + 600], fill=PANEL)
    d.text((22, y1 + 8), 'DORIAN PELL - Gym 1 Warden (Normal), 56, ex-matinee idol: dashing, vain, theatrical. "The curtain call that never ended."', font=FB(15), fill=GOLD)
    label(d, (22, y1 + 32), '1  Silhouettes: battle fronts from sheet 18 (S chosen there) and five bust ideas for the portrait, filled black at true size.')
    x = 22
    for n in ('dor_A', 'dor_B', 'dor_S'):
        im = kb.load(G + 'art/work/kitbash/passes/%s.png' % n)
        S.alpha_composite(plate(black(im), 2, CREAM), (x, y1 + 52)); label(d, (x, y1 + 222), {'dor_S': 'front S (chosen)'}.get(n, 'front ' + n[-1]), F(12), GOLD if n == 'dor_S' else DIM)
        x += 176
    for n in dp.SIL:
        S.alpha_composite(plate(dp.silhouette(n), 2, CREAM), (x, y1 + 52))
        label(d, (x, y1 + 160), n, F(12), GOLD if 'chosen' in n else DIM); x += 112
    notes = ['A: swept-back mane = vanity + motion; reads at 1x', 'B: generic; C: hat hides the hair, and he holds it',
             'D: reads young (quiff); E: long mane reads vampire', '   with plum + high collar (rejected Juggler lesson)']
    for i, t in enumerate(notes): label(d, (x - 560, y1 + 180 + i * 15), t, F(11))
    yb = y1 + 246
    label(d, (22, yb), '2  Chosen design (front S, 80-px art) and the portrait colour plan: 3 colours + 1 accent')
    fr = kb.load(G + 'art/work/kitbash/dorian/DORIAN_S_native80.png')
    S.alpha_composite(plate(fr, 3, CREAM), (22, yb + 20))
    swatches(d, 280, yb + 24, [('1 plum velvet', list(dp.COAT)), ('2 silver (hair,', list(dp.HAIR) + ['4a4274']), ('   satin lining)', []),
                               ('3 ivory silk', list(dp.IVORY)), ('accent: rose', ['ff8a96', 'e33a4c', 'a51d36', '6a1028']),
                               ('skin', list(dp.SK)), ('eyes / brows', ['dc9a36', '8a4c1c', '3e3656']), ('outline', ['1a1220'])])
    label(d, (280, yb + 206), 'Saltmere (Elowen free port): no kingdom green on him;', F(11))
    label(d, (280, yb + 221), 'his motif is the theatre: velvet, satin, the rose.', F(11))
    xp = 760
    label(d, (xp, yb), '3  Portrait: original construction (guide 3.11) - shapes -> light from upper left -> lines -> features. No donor pixels.')
    S.alpha_composite(plate(dk, 5, WIN), (xp, yb + 20)); label(d, (xp, yb + 270), 'knowing (default), 5x', F(12), GOLD)
    for i, (im, n) in enumerate([(dk, 'knowing'), (dl, 'laugh'), (ds, 'surprised')]):
        S.alpha_composite(plate(im, 2, WIN), (xp + 258 + i * 108, yb + 20)); label(d, (xp + 258 + i * 108, yb + 124), n, F(11))
        S.alpha_composite(plate(im, 2, CREAM), (xp + 258 + i * 108, yb + 142))
    label(d, (xp + 258, yb + 246), 'true size (96x96) on the window plate and on cream', F(11))
    v1 = G + 'art/work/kitbash/passes/faces_v1/DORIAN_neutral_48.png'
    if os.path.exists(v1):
        S.alpha_composite(plate(kb.load(v1), 2, WIN), (xp + 600, yb + 20)); label(d, (xp + 600, yb + 124), 'faces_v1 (sheet 26)', F(11))
        label(d, (xp + 600, yb + 138), 'for comparison only', F(11))
    chk = ['Guide checks:', '- silhouette: mane + crest + one lock', '- 4 hair tones + crease + 1 arc/clump', '- brows B2 + B3 (far one arched), J3 jaw, E3 eyes',
           '- mouths: line / D-shape with teeth /', '  dark oval - never a red dot', '- moustache: 1 crisp line, 2 tones', '- 29 colours (<= 32); outline #1a1220',
           '- "who does it look like?": checked', '  vs Grimsley, Drayden, Lysandre,', '  Wallace, Volkner: no match']
    for i, t in enumerate(chk): label(d, (xp + 720, yb + 20 + i * 16), t, F(11), INK if i == 0 else DIM)

    # ---------------- in-game mock ----------------
    y2 = y1 + 612
    d.rectangle([10, y2, W - 10, H - 10], fill=PANEL)
    d.text((22, y2 + 8), 'True size in the Desolation-style face window (Rev 22): 512x384 screen, 96x96 face in a 128x128 box above the message box', font=FB(15), fill=GOLD)
    MP = G + 'maps_out/previews/'
    def scene(f, box):
        return Image.open(MP + f).convert('RGBA').crop(box) if os.path.exists(MP + f) else None
    m1 = face_window_mock(up(jref, 2), 'Juno', 'Did you know larches drop their needles', "every winter? They're not dead!",
                          scene('100_Ferrow_s_Landing.png', (1284, 1508, 1796, 1892)))
    m2 = face_window_mock(up(dk, 2), 'Dorian', 'Enter, stage left, our brave challenger!', 'The house is yours, darling.',
                          scene('154_Pell_Playhouse___Auditorium.png', (144, 40, 656, 424)))
    m3 = face_window_mock(up(dl, 2), 'Dorian', 'Ha! The house loves a show -', 'and so, I confess, do I.',
                          scene('154_Pell_Playhouse___Auditorium.png', (144, 40, 656, 424)))
    S.alpha_composite(m1, (22, y2 + 36)); S.alpha_composite(m2, (22 + 530, y2 + 36)); S.alpha_composite(m3, (22 + 1060, y2 + 36))
    S.convert('RGB').save(OUT, optimize=True)
    print(OUT, S.size)


if __name__ == '__main__':
    main()
