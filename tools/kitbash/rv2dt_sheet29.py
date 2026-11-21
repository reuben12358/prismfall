"""Review sheet 29: redo v2 of Dorian Pell (Gym 1) and Tamsin Loom (Gym 2), beside Juno (the approved anchor).
python3 -I tools/kitbash/rv2dt_sheet29.py  -> art/previews/29_redo_dorian_tamsin.png (nothing is installed)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import rv2dt_dorian as D
import rv2dt_tamsin as T
from rv2dt_px import up, hx, lint, colours

G = '/home/claude/fangame/'
OUT = G + 'art/previews/29_redo_dorian_tamsin.png'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
GAMEF = '/home/claude/ref/ebdx/Fonts/power green narrow.ttf'
F = lambda n: ImageFont.truetype(FONT, n)
FB = lambda n: ImageFont.truetype(FONTB, n)
BG, PANEL, INK, DIM, GOLD = (30, 30, 38, 255), (44, 44, 54, 255), (236, 236, 240, 255), (182, 182, 194, 255), (244, 208, 120, 255)
CREAM, WIN, FIELD = (232, 226, 212, 255), (52, 56, 74, 255), (112, 150, 104, 255)


def load(p): return Image.open(p).convert('RGBA')


def plate(im, k, bg, pad=4):
    b = Image.new('RGBA', (im.width * k + pad * 2, im.height * k + pad * 2), bg)
    b.alpha_composite(up(im, k), (pad, pad)); return b


def text(d, xy, t, f=None, fill=DIM):
    d.text(xy, t, font=f or F(12), fill=fill)


def para(d, x, y, lines, f=None, fill=DIM, lh=15):
    for i, t in enumerate(lines):
        d.text((x, y + i * lh), t, font=f or F(12), fill=INK if t.endswith(':') and len(t) < 40 else fill)
    return y + len(lines) * lh


def swatches(d, x, y, groups):
    for gi, (name, cols) in enumerate(groups):
        yy = y + gi * 22
        text(d, (x, yy + 3), name, F(11), INK)
        for i, c in enumerate(cols):
            d.rectangle([x + 128 + i * 20, yy, x + 146 + i * 20, yy + 18], fill=hx(c), outline=(0, 0, 0, 255))


def demagenta(im):
    """map previews carry magenta event markers: replace them with the pixel one tile to the left"""
    im = im.copy(); p = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = p[x, y]
            if r > 200 and b > 200 and g < 80:
                for dx in (32, -32, 64, -64):
                    if 0 <= x - dx < im.width:
                        q = p[x - dx, y]
                        if not (q[0] > 200 and q[2] > 200 and q[1] < 80): p[x, y] = q; break
    return im


def face_window_mock(portrait96, name, line1, line2, scene, walker=None, wpos=None):
    """Essentials face window, Desolation layout (Rev 22): 128x128 box, 96x96 face, left, above the message box.
    walker: one 32x48 charset frame drawn on the map at true size."""
    W, H = 512, 384
    m = Image.new('RGBA', (W, H), (70, 90, 120, 255)); m.alpha_composite(scene.crop((0, 0, W, H)))
    if walker is not None: m.alpha_composite(walker, wpos)
    d = ImageDraw.Draw(m)
    d.rectangle([8, 188, 136, 316], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=3)
    d.rectangle([16, 196, 128, 308], fill=WIN)
    m.alpha_composite(portrait96, (24, 204))
    d.rectangle([8, 320, 504, 378], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=3)
    gf = ImageFont.truetype(GAMEF, 24); nf = ImageFont.truetype(GAMEF, 20)
    d.text((22, 324), line1, font=gf, fill=(72, 72, 80, 255)); d.text((22, 349), line2, font=gf, fill=(72, 72, 80, 255))
    d.rectangle([8, 158, 8 + 14 + int(d.textlength(name, font=nf)), 184], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=2)
    d.text((15, 160), name, font=nf, fill=(56, 90, 160, 255))
    return m


def battle_mock(front160, bgfile, base_xy, line):
    """EBDX intro framing (as the engine capture art/previews/11_juno_everbloom_engine.png): the field's battlebg
    drawn about 2x, the 160x160 front anchored bottom-centre on the far base, the intro message box."""
    bg = load(G + 'graphics/EBDX/Battlebacks/battlebg/' + bgfile)
    big = bg.resize((bg.width * 2, bg.height * 2), Image.NEAREST)
    bx, by = base_xy
    x0, y0 = bx * 2 - 365, by * 2 - 196
    m = big.crop((x0, y0, x0 + 512, y0 + 384)).convert('RGBA')
    m.alpha_composite(front160, (365 - 80, 206 - 160))
    ov = Image.new('RGBA', (512, 384), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle([16, 298, 496, 368], 6, fill=(60, 56, 52, 205))
    m.alpha_composite(ov); d = ImageDraw.Draw(m)
    d.text((36, 312), line, font=ImageFont.truetype(GAMEF, 26), fill=(248, 248, 248, 255))
    return m


def expr_diff(mod):
    """guide 3.9: expressions change only brows, eyes, mouth and marks. Bounding box of changed pixels vs neutral."""
    base = mod.portrait_img('neutral'); out = []
    for e in mod.PORTRAIT_EXPRS[1:]:
        im = mod.portrait_img(e); p, q = base.load(), im.load()
        ch = [(x, y) for y in range(48) for x in range(48) if p[x, y] != q[x, y]]
        if ch:
            xs, ys = [c[0] for c in ch], [c[1] for c in ch]
            out.append('%s: %d px in x%d-%d y%d-%d' % (e, len(ch), min(xs), max(xs), min(ys), max(ys)))
    return out


def character(S, y0, mod, info):
    d = ImageDraw.Draw(S)
    H = info['height']
    d.rectangle([10, y0, S.width - 10, y0 + H], fill=PANEL)
    d.text((22, y0 + 8), info['title'], font=FB(16), fill=GOLD)
    text(d, (22, y0 + 32), info['sub'], F(12))
    # ---- 1 silhouettes
    yy = y0 + 56
    text(d, (22, yy), '1  Silhouettes at true size (80-px fronts filled black), the pick first. Reason for each rejection under it.', F(12), INK)
    x = 22
    for i, (lab, im, why) in enumerate(mod.silhouettes()):
        S.alpha_composite(plate(im, 1, CREAM, 6), (x, yy + 20))
        text(d, (x, yy + 116), lab, F(11), GOLD if i == 0 else INK)
        words, line, ln = why.split(), '', 0
        for w in words:
            if d.textlength(line + ' ' + w, font=F(10)) > 236:
                text(d, (x, yy + 132 + ln * 13), line.strip(), F(10)); line, ln = '', ln + 1
            line += ' ' + w
        text(d, (x, yy + 132 + ln * 13), line.strip(), F(10))
        x += 250 if i < 7 else 0
    # ---- 2 chosen design + colour plan
    yy = y0 + 230
    text(d, (22, yy), '2  Chosen design and colour plan (3 colours + 1 accent, light from the upper left)', F(12), INK)
    fr = mod.front_img()
    S.alpha_composite(plate(fr, 3, CREAM), (22, yy + 20))
    swatches(d, 280, yy + 22, info['swatches'])
    para(d, 280, yy + 22 + 22 * len(info['swatches']) + 8, info['design'], F(11))
    # ---- 3 battle front
    xb = 820
    text(d, (xb, yy), '3  Battle front: 80-px art, 160x160 file (shown at 2x = in-game size)', F(12), INK)
    f2 = up(fr, 2)
    S.alpha_composite(plate(f2, 1, CREAM), (xb, yy + 20))
    S.alpha_composite(plate(f2, 1, FIELD), (xb + 172, yy + 20))
    old = load(info['old'])
    S.alpha_composite(plate(old, 1, CREAM), (xb + 344, yy + 20))
    text(d, (xb, yy + 190), 'new, on cream', F(11), GOLD); text(d, (xb + 172, yy + 190), 'new, on the field', F(11))
    text(d, (xb + 344, yy + 190), info['old_label'], F(11))
    juno = load(G + 'art/out/Graphics/Trainers/RIVAL_JUNO.png')
    S.alpha_composite(plate(juno, 1, CREAM), (xb + 516, yy + 20)); text(d, (xb + 516, yy + 190), 'Juno (approved anchor)', F(11))
    # line-up at native 1x: the size the silhouette must survive
    lu = Image.new('RGBA', (360, 90), FIELD)
    for i, im in enumerate([fr, load(G + 'art/work/redo_v2/DORIAN/Trainers/LEADER_DORIAN_native80.png') if mod is T else
                            load(G + 'art/work/redo_v2/TAMSIN/Trainers/LEADER_TAMSIN_native80.png'),
                            juno.resize((80, 80), Image.NEAREST), old.resize((80, 80), Image.NEAREST)]):
        lu.alpha_composite(im, (6 + i * 88, 5))
    S.alpha_composite(lu, (xb, yy + 212)); text(d, (xb + 368, yy + 212), '1x line-up: new | the other new', F(11))
    text(d, (xb + 368, yy + 228), 'Warden | Juno | previous', F(11))
    n, semi, orph = lint(fr)
    text(d, (xb + 368, yy + 250), 'front: %d colours (cap 36), %d semi-alpha, %d orphans' % (n, semi, len(orph)), F(11), INK)
    # ---- 4 portraits
    yy = y0 + 590
    text(d, (22, yy), '4  Portraits: 48-px art, 96x96 files. One base face; expressions swap brow / eye / mouth stamps only.', F(12), INK)
    x = 22
    for e in mod.PORTRAIT_EXPRS:
        im = mod.portrait_img(e)
        S.alpha_composite(plate(up(im, 2), 2, WIN, 3), (x, yy + 20))
        S.alpha_composite(plate(up(im, 2), 1, WIN, 3), (x + 50, yy + 220))
        S.alpha_composite(plate(up(im, 2), 1, CREAM, 3), (x + 50, yy + 324))
        text(d, (x, yy + 220), e + (' *' if e == info['signature'] else ''), F(12), GOLD if e == info['signature'] else INK)
        x += 206
    para(d, 1262, yy + 24, ['Top row: 2x (192 px).', 'Below: 1x, the true 96x96 size,', 'on the window plate and on cream.',
                            '* = signature expression', '', 'Face kit: ' + info['kit']], F(11))
    # ---- 5 overworld
    yy = y0 + 1020
    text(d, (22, yy), '5  Overworld: 4x4 frames, 32x48 per frame = 16x24 art doubled (as JUNO.png); rows down / left / right / up.', F(12), INK)
    ow = mod.ow_sheet()
    S.alpha_composite(plate(ow, 3, CREAM), (22, yy + 20))
    S.alpha_composite(plate(up(ow, 2), 1, CREAM), (232, yy + 20))
    jow = load(G + 'art/out/Graphics/Characters/JUNO.png')
    S.alpha_composite(plate(jow, 1, CREAM), (380, yy + 20))
    text(d, (22, yy + 318), 'frames at 3x | in-game (2x) | Juno', F(11))
    n, semi, orph = lint(ow)
    text(d, (232, yy + 222), '%d colours (cap 24)' % n, F(11), INK)
    text(d, (232, yy + 236), 'walk: stand, step, stand,', F(11)); text(d, (232, yy + 250), 'step; step frames bob 1 row', F(11))
    text(d, (232, yy + 264), 'like Juno\'s sheet', F(11))
    # walk strip at 1x on a grass plate
    strip = Image.new('RGBA', (4 * 34 + 4, 4 * 50 + 4), FIELD)
    big = up(ow, 2)
    for r in range(4):
        for c in range(4):
            strip.alpha_composite(big.crop((c * 32, r * 48, c * 32 + 32, r * 48 + 48)), (4 + c * 34, 4 + r * 50))
    S.alpha_composite(strip, (530, yy + 20)); text(d, (530, yy + 228), 'in-game size, on grass', F(11))
    # ---- 6 mocks
    xm = 700
    text(d, (xm, yy), '6  True size (512x384 screen): dialogue face window on our map, and the EBDX battle intro', F(12), INK)
    S.alpha_composite(info['mock_dialogue'], (xm, yy + 20))
    S.alpha_composite(info['mock_battle'], (xm + 524, yy + 20))
    # ---- 7 checks
    yy = y0 + 1450
    text(d, (22, yy), '7  Checks', F(12), INK)
    para(d, 22, yy + 20, info['checks'], F(11))
    para(d, 700, yy + 20, ['Expression diff vs neutral (guide 3.9: only brows, eyes, mouth, marks move):'] + expr_diff(mod), F(11))
    para(d, 1240, yy + 20, info['weak'], F(11))


def main():
    W = 1900
    S = Image.new('RGBA', (W, 3600), BG); d = ImageDraw.Draw(S)
    d.text((16, 10), 'SHEET 29 - Redo v2: Dorian Pell (Gym 1) and Tamsin Loom (Gym 2), original construction, beside Juno', font=FB(18), fill=INK)
    text(d, (16, 38), 'Brief: art/REDO_V2_BRIEF.md. Rules: art/STYLE_GUIDE.md. Recipes: tools/kitbash/rv2dt_{px,dorian,tamsin,sheet29}.py. '
                      'Files: art/work/redo_v2/{DORIAN,TAMSIN}/ in the Graphics layout. Nothing installed.', F(12))
    # ---- Juno reference strip
    y = 62
    d.rectangle([10, y, W - 10, y + 262], fill=PANEL)
    d.text((22, y + 8), 'JUNO HALE - the approved quality anchor (unchanged)', font=FB(15), fill=GOLD)
    S.alpha_composite(plate(load(G + 'art/out/Graphics/Trainers/RIVAL_JUNO.png'), 1, CREAM), (22, y + 34))
    jow = Image.open(G + 'art/out/Graphics/Characters/JUNO.png').convert('RGBA').resize((64, 96), Image.NEAREST)
    S.alpha_composite(plate(jow.crop((0, 0, 64, 24)), 3, CREAM), (200, y + 34))
    x = 200
    for i, e in enumerate(('neutral', 'happy', 'sad', 'surprised', 'wink')):
        im = load(G + 'art/out/Graphics/Portraits/JUNO_%s.png' % e)
        S.alpha_composite(plate(im, 1, WIN, 3), (x + i * 108, y + 136)); text(d, (x + i * 108, y + 238), e, F(11))
    text(d, (200, y + 118), 'battle 160x160 (2x) | walk frames at 3x | portraits 96x96 (1x)', F(11))
    text(d, (800, y + 40), 'What the new art matches: 1-px near-black outline, 2-3 flat tones per material, big readable', F(12), INK)
    text(d, (800, y + 58), 'eyes with one catchlight, warm saturated colour, about 25-32 colours per piece, no noise.', F(12), INK)
    text(d, (800, y + 86), 'Face kit (guide 2.3), main cast so far:', F(12), INK)
    for i, t in enumerate(['Juno    J1 round  + E1 big round        + B1 soft',
                           'Kestrel J2 sharp V + E2 almond          + B2 strong',
                           'Dorian  J3 square + E3 hooded (amber)   + B2 near / B3 arched far brow, pencil moustache',
                           'Tamsin  J2 soft V + E1 droop-cornered (violet) + B1 soft, inner ends raised (always a little worried)']):
        d.text((800, y + 106 + i * 17), t, font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12), fill=DIM)
    text(d, (800, y + 182), 'No two share a jaw + eye + brow combination.', F(12))

    # ---- mocks
    pp = demagenta(load(G + 'maps_out/previews/154_Pell_Playhouse___Auditorium.png')).crop((144, 40, 656, 424))
    lob = demagenta(load(G + 'maps_out/previews/130_Loomhouse_Gym___Lobby.png')).crop((64, 64, 576, 448))
    dow = up(D.ow_sheet(), 2).crop((0, 0, 32, 48)); tow = up(T.ow_sheet(), 2).crop((0, 0, 32, 48))
    dm = face_window_mock(up(D.portrait_img('laugh'), 2), 'Dorian', 'Enter, stage left, our brave challenger!',
                          'The house is yours, darling.', pp, dow, (300, 120))
    tm = face_window_mock(up(T.portrait_img('flustered'), 2), 'Tamsin', "Sorry - sorry - the Silkwood's a bit",
                          'tangled today. Like me.', lob, tow, (290, 150))
    db = battle_mock(up(D.front_img(), 2), 'field_grand_stage.png', (233, 153), 'Warden Dorian would like to battle!')
    tb = battle_mock(up(T.front_img(), 2), 'field_silkwood.png', (233, 153), 'Warden Tamsin would like to battle!')

    dinfo = dict(height=1590, signature='laugh', kit='J3 + E3 + B2/B3',
                 title='DORIAN PELL - Gym 1 Warden (Normal), 56, ex-matinee idol. "The curtain call that never ended."',
                 sub='Built from the style-test portrait (sheet 27): cleaned shading (no speckled cheek/chin), head lowered to close the crown in frame, '
                     'E3 eyes at full 3-row opening, five expressions + laugh.',
                 swatches=[('1 plum velvet', D.PLUM), ('2 silver (hair, satin)', D.HAIR), ('3 ivory silk', D.IVORY),
                           ('accent: rose', D.ROSE), ('trousers/hat', D.TROU), ('skin', D.SKIN), ('eyes', (D.IRIS, D.IRIS_D, D.EYE_W)),
                           ('outline', (D.K,))],
                 design=['Hook (only his): the swept-back silver mane, crest up front, clumps', 'flaring back to tapered tips; it shows from all 4 sides.',
                         'Pose: top hat aloft in a toast to the house, the silver-topped', "cane he doesn't need held out like a prop: one diagonal",
                         'from hat to cane tip. Kept from pick S: the hat aloft.', 'Changed from S: own body and pose (S was Sycamore\'s arms-wide).',
                         'Normal = the everyday made theatre: velvet, satin, the rose.', 'Saltmere is a free port: no kingdom green on him.',
                         'Accent: the rose (lapel); from the back the satin lining edge.'],
                 old=G + 'art/work/kitbash/dorian/DORIAN_S.png', old_label='previous: pick S (kitbash)',
                 mock_dialogue=dm, mock_battle=db,
                 checks=['Who does it look like? Checked against Grimsley (scarf, robe), Drayden (white beard,', 'crossed arms), Lysandre (orange lion mane), Wallace (cape, aqua),',
                         'Volkner (blond spikes), Sycamore (arms-wide pose: dropped), Ingo/Emmet', '(long coats, caps): no match. Silver hair + violet eyes = Bede: his eyes are amber.',
                         'Long mane + plum + high collar = vampire: no high collar, no cape.', 'Portraits: 96x96, 2x2 blocks, alpha 0/255, 24-26 colours, eye line 25, chin 41,',
                         'crown closes at row 2, faces right, >= 2 px air at the right. No orphans.', 'Hair: 5 clumps, 1 arc each, creases in the deepest hair tone, no black strands.',
                         'Mouths: line + corners (neutral, happy, sad); outlined holes (angry, surprised, laugh).'],
                 weak=['Weak spots (honest):', '- The front is built from shapes, not a pro body: the legs and the', '  coat skirt are stiffer than an official sprite.',
                       '- At 1x the mane can read "wild professor" rather than groomed;', '  the portrait carries the groomed read better.',
                       '- Portrait: the face is a large flat plane (adult, hooded eyes);', '  it is clean but less lively than Juno\'s big-eyed face.'])
    tinfo = dict(height=1590, signature='flustered', kit='J2 + E1 (droop) + B1',
                 title='TAMSIN LOOM - Gym 2 Warden (Bug), 19, Briarwick\'s weaver. "The girl wrapped in her grandmother\'s last weave."',
                 sub='Kept from pick A: Granny Loom\'s moth-wing shawl, the measuring tape, needles through a messy bun, worried brows. '
                     'Changed: the shawl is silk cream with a gold border (the brown wings read muddy); one wing is spread, one wraps her.',
                 swatches=[('1 silk cream (shawl)', T.SILK), ('2 indigo linen', T.INDIGO), ('3 lantern gold', T.GOLD),
                           ('accent: berry thread', T.BERRY), ('hair (cocoa-rose)', T.HAIR), ('skin', T.SKIN),
                           ('eyes', (T.IRIS, T.IRIS_D, T.EYE_W)), ('outline', (T.K,))],
                 design=['Hook (only hers): the moth-wing shawl, one wing spread like a moth', 'showing its pattern, the other wrapped round her; the bun with two',
                         'knitting needles reads as antennae. Pose: shy and showing at once,', 'knees together, toes in, an apologetic smile and a sweat drop.',
                         'Bug = thread and silk (the shawl, the spool), never the uniform: Bug', 'green is not used. Elowen = cream linen + lantern-gold thread',
                         '(border, tape, embroidered hem). Indigo is the weaver\'s dye.', 'Accent: one berry-red thread: the spool at her chest (front) and',
                         'the thread wound round her bun (back). Ink on her fingertips.'],
                 old=G + 'art/work/kitbash/tamsin/TAMSIN_A.png', old_label='previous: pick A (kitbash)',
                 mock_dialogue=tm, mock_battle=tb,
                 checks=['Who does it look like? Checked against Burgh (curly brown hair, green,', 'arms wide), Katy (mint hair, beret, brown apron), Bugsy (purple hair, net),',
                         'Lacey (pink hair, lilac coat), Viola (camera, blonde), Juno (ivory + pink:', 'Tamsin is cream + indigo + gold), Thistle/Mourner (hoods: none here). No match.',
                         'Portraits: 96x96, 2x2 blocks, alpha 0/255, 22-24 colours, eye line 25, chin 42,', 'whole head in frame, faces right, >= 2 px air at the right. No orphans.',
                         'Hair: mass + bun + 3 fringe locks + side lock, 1 arc each, creases in the', 'darkest hair tone (not black). Mouths: line (neutral, sad), open holes',
                         '(happy, surprised, angry with teeth rows, flustered).'],
                 weak=['Weak spots (honest):', '- The front is built from shapes: the dress is a large flat indigo', '  area and the pose is stiffer than an official sprite.',
                       '- The spread wing reads strongly but flat; it has one band and one', '  eyespot by design (restraint), so it is plain up close.',
                       '- Her head sits smaller in the portrait frame than Juno\'s (a bun,', '  not a mane), so the frame feels emptier.'])
    character(S, 336, D, dinfo)
    character(S, 336 + 1602, T, tinfo)
    S = S.crop((0, 0, W, 336 + 1602 * 2 + 4))
    S.convert('RGB').save(OUT, optimize=True)
    print(OUT, S.size)


if __name__ == '__main__':
    main()
