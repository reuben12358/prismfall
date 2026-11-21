"""Sheet 29 + exports: redo v2 of Kestrel Vane and Professor Larch (brief art/REDO_V2_BRIEF.md). Nothing is installed.
Exports go to art/work/redo_v2/<NAME>/Graphics/{Trainers,Characters,Portraits}/ in the game's file layout (+ native/).
python3 -I tools/kitbash/rv2kl_sheet29.py [export|sheet|all]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'art', 'research', 'scripts'))
import kb
import rv2kl_kestrel as KE
import rv2kl_larch as LA
from rv2kl_lib import up, lint, black, hx, G
from PIL import Image, ImageDraw, ImageFont

OUT = G + 'art/previews/29_redo_kestrel_larch.png'
F = lambda n: kb.font(n)
FB = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', n)
GAMEF = '/home/claude/ref/ebdx/Fonts/power green narrow.ttf'
BG, PANEL, INK, DIM, GOLD = (30, 30, 38, 255), (44, 44, 54, 255), (236, 236, 240, 255), (180, 180, 192, 255), (244, 208, 120, 255)
CREAM, WIN, FIELD = (232, 226, 212, 255), (52, 56, 74, 255), (112, 150, 104, 255)
JUNO = G + 'art/out/Graphics/'

CHARS = {
    'KESTREL': dict(mod=KE, trainer='RIVAL_KESTREL', ow='KESTREL', ow_alias=['trainer_RIVAL_KESTREL'], portrait='KESTREL',
                    aliases={'shocked': 'surprised'}),
    'LARCH': dict(mod=LA, trainer='LARCH', ow='LARCH', ow_alias=['trainer_LARCH'], portrait='LARCH', aliases={}),
}


def export():
    rep = {}
    for key, d in CHARS.items():
        m = d['mod']; base = G + 'art/work/redo_v2/%s/' % key
        for sub in ('Graphics/Trainers', 'Graphics/Characters', 'Graphics/Portraits', 'native'):
            os.makedirs(base + sub, exist_ok=True)
        fr = m.front().image()
        fr.save(base + 'native/%s_native80.png' % d['trainer']); up(fr, 2).save(base + 'Graphics/Trainers/%s.png' % d['trainer'])
        ow = m.overworld()
        ow.save(base + 'Graphics/Characters/%s.png' % d['ow'])
        for a in d['ow_alias']: ow.save(base + 'Graphics/Characters/%s.png' % a)
        ow.resize((64, 96), Image.NEAREST).save(base + 'native/%s_ow_native.png' % d['ow'])
        faces = {}
        for e in m.PORTRAIT_EXPRS:
            im = m.portrait(e).image(); faces[e] = im
            im.save(base + 'native/%s_%s_48.png' % (d['portrait'], e))
            up(im, 2).save(base + 'Graphics/Portraits/%s_%s.png' % (d['portrait'], e))
        up(faces['neutral'], 2).save(base + 'Graphics/Portraits/%s.png' % d['portrait'])
        for a, b in d['aliases'].items():
            up(faces[b], 2).save(base + 'Graphics/Portraits/%s_%s.png' % (d['portrait'], a))
        rep[key] = {'front': lint(fr), 'ow': lint(ow), 'faces': {e: lint(i)['colours'] for e, i in faces.items()},
                    'face_orphans': {e: len(lint(i)['orphans']) for e, i in faces.items()}}
    return rep


# ------------------------------------------------------------------------------------------------------------------
def plate(im, k, bg, pad=4):
    b = Image.new('RGBA', (im.width * k + pad * 2, im.height * k + pad * 2), bg)
    b.alpha_composite(up(im, k), (pad, pad)); return b


def label(d, xy, t, f=None, fill=DIM):
    d.text(xy, t, font=f or F(12), fill=fill)


def swatches(d, x, y, groups, w=178):
    for gi, (name, cols) in enumerate(groups):
        yy = y + gi * 21
        label(d, (x, yy + 3), name, F(11), INK)
        for i, c in enumerate(cols):
            d.rectangle([x + w + i * 19, yy, x + w + 17 + i * 19, yy + 17], fill=hx(c), outline=(0, 0, 0, 255))


def demagenta(im):
    """map previews carry magenta event boxes: paint them with the pixel 3 to the left."""
    im = im.convert('RGBA'); p = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = p[x, y]
            if r > 200 and g < 60 and b > 200: p[x, y] = p[max(0, x - 3), y]
    return im


def face_window_mock(portrait96, name, line1, line2, bgimg=None, ow=None, owxy=None):
    W, H = 512, 384
    m = Image.new('RGBA', (W, H), (70, 90, 120, 255))
    if bgimg is not None: m.alpha_composite(bgimg.crop((0, 0, W, H)))
    if ow is not None: m.alpha_composite(ow, owxy)
    d = ImageDraw.Draw(m)
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


def battle_mock(trainer160, line):
    """EBDX intro framing (cf. art/previews/11_juno_everbloom_engine.png): 512x384, trainer 160x160 anchored
    bottom-centre on the foe base, message box at the bottom."""
    bg = Image.open(G + 'graphics/EBDX/Battlebacks/battlebg/field_meadow_hd.png').convert('RGBA')
    bg = bg.resize((512, int(bg.height * 512 / bg.width)), Image.LANCZOS)
    m = Image.new('RGBA', (512, 384), (0, 0, 0, 255)); m.alpha_composite(bg.crop((0, 0, 512, 384)))
    d = ImageDraw.Draw(m)
    d.ellipse([290, 192, 430, 222], fill=(150, 190, 110, 255))
    d.ellipse([20, 330, 220, 372], fill=(150, 190, 110, 255))
    m.alpha_composite(trainer160, (360 - 80, 212 - 160))
    d.rectangle([16, 296, 496, 372], fill=(70, 64, 60, 235), outline=(40, 36, 34, 255), width=2)
    try: gf = ImageFont.truetype(GAMEF, 24)
    except Exception: gf = F(16)
    d.text((36, 312), line, font=gf, fill=(248, 248, 248, 255))
    return m


def ow_frames_strip(sheet128, k):
    n = sheet128.resize((64, 96), Image.NEAREST)
    out = Image.new('RGBA', (4 * 16 * k + 3 * 4, 4 * 24 * k + 3 * 4), (0, 0, 0, 0))
    for r in range(4):
        for c in range(4):
            out.alpha_composite(up(n.crop((c * 16, r * 24, c * 16 + 16, r * 24 + 24)), k), (c * (16 * k + 4), r * (24 * k + 4)))
    return out


def char_panel(S, d, y0, key, info):
    m = info['mod']; W = S.width
    d.rectangle([10, y0, W - 10, y0 + info['h']], fill=PANEL)
    d.text((22, y0 + 8), info['title'], font=FB(15), fill=GOLD)
    label(d, (22, y0 + 30), info['concept'], F(12), INK)
    # 1 silhouettes
    yb = y0 + 54
    label(d, (22, yb), '1  Silhouettes (80-px front, black, 2x and 1x on cream). Hook: ' + info['hook'], F(12), INK)
    x = 22
    for i, s in enumerate(m.SILS):
        im = m.silhouette(i); name, why = s[0], s[-1]
        S.alpha_composite(plate(im, 2, CREAM, 2), (x, yb + 20))
        S.alpha_composite(plate(im, 1, CREAM, 2), (x + 168, yb + 20))
        label(d, (x, yb + 188), name, F(12), GOLD if 'chosen' in name else DIM)
        for j, ln in enumerate(wrap(why, 34)): label(d, (x, yb + 204 + j * 14), ln, F(10))
        x += 258 if i < 3 else 0
        if i == 3: x = 22; yb2 = yb + 250
        if i > 3:
            pass
    return


def wrap(t, n):
    out, cur = [], ''
    for w in t.split():
        if len(cur) + len(w) + 1 > n: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    if cur: out.append(cur)
    return out


def sil_row(S, d, x, y, m, cell=172):
    for i, s in enumerate(m.SILS):
        im = m.silhouette(i); name, why = s[0], s[-1]
        S.alpha_composite(plate(black(im), 2, CREAM, 2), (x + i * cell, y))
        S.alpha_composite(plate(black(im), 1, CREAM, 2), (x + i * cell + 82, y + 166 - 84))
        label(d, (x + i * cell, y + 170), name, F(12), GOLD if 'chosen' in name else DIM)
        for j, ln in enumerate(wrap(why, 26)): label(d, (x + i * cell, y + 186 + j * 13), ln, F(10))


def sheet():
    jf = kb.native(kb.load(JUNO + 'Trainers/RIVAL_JUNO.png'))[0]
    jow = Image.open(JUNO + 'Characters/JUNO.png').convert('RGBA')
    jn = kb.native(kb.load(JUNO + 'Portraits/JUNO_neutral.png'))[0]
    jh = kb.native(kb.load(JUNO + 'Portraits/JUNO_happy.png'))[0]
    W, H = 2200, 3800
    S = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(S)
    d.text((16, 10), 'SHEET 29 - REDO V2: Kestrel Vane (rival) and Professor Imelda Larch (mentor). Original construction, nothing installed.',
           font=FB(18), fill=INK)
    label(d, (16, 38), 'Per art/STYLE_GUIDE.md: silhouettes -> chosen design + 3+1 palette -> 80-px front (shown 2x) -> 16x24 overworld '
          '(shown 3x) -> 48-px portraits (2x = the 96x96 file, and 1x). Files: art/work/redo_v2/{KESTREL,LARCH}/Graphics/... '
          'Recipes: tools/kitbash/rv2kl_*.py', F(12))
    # ---------------- Juno reference strip ----------------
    y = 62
    d.rectangle([10, y, W - 10, y + 300], fill=PANEL)
    d.text((22, y + 8), 'REFERENCE - Juno Hale (approved, unchanged): battle 2x, overworld 3x, portraits 2x and 1x', font=FB(15), fill=GOLD)
    S.alpha_composite(plate(jf, 2, FIELD), (22, y + 34))
    S.alpha_composite(ow_frames_strip(jow, 3).crop((0, 0, 4 * 52, 76)), (200, y + 34))
    S.alpha_composite(ow_frames_strip(jow, 3).crop((0, 152, 4 * 52, 228)), (200, y + 116))
    for i, im in enumerate((jn, jh)):
        S.alpha_composite(plate(im, 2, WIN), (430 + i * 110, y + 34))
        S.alpha_composite(plate(im, 1, WIN), (430 + i * 110, y + 144))
    label(d, (430, y + 206), 'neutral | happy (installed, pass 3)', F(11))
    label(d, (680, y + 40), 'What "Juno finish" means on this sheet (and what we matched):', F(12), INK)
    for i, t in enumerate(['- black/near-black 1-px outline, flat 2-3 tones per material, no dithering or noise',
                           '- big readable eyes with one hard catchlight; mouths as shapes',
                           '- bright, saturated base colours; every portrait <= 32 colours, alpha 0/255 only',
                           '- 160x160 trainer file (80-px art doubled), feet 2-3 px off the bottom; 128x192 charset (16x24 doubled)',
                           '- 96x96 portraits = 48-px art doubled, eye line 22-27, chin 40-44, whole head in frame, facing right']):
        label(d, (680, y + 62 + i * 18), t, F(12))
    # line-up at 1x on the field
    lu = Image.new('RGBA', (560, 96), FIELD)
    for i, im in enumerate([jf, KE.front().image(), LA.front().image()]):
        lu.alpha_composite(im, (20 + i * 120, 8))
    S.alpha_composite(lu, (1600, y + 40))
    label(d, (1600, y + 140), '1x line-up on the battle field: Juno | Kestrel | Larch', F(11))
    jo = Image.new('RGBA', (300, 60), FIELD)
    for i, im in enumerate([jow, KE.overworld(), LA.overworld()]):
        jo.alpha_composite(im.crop((0, 0, 32, 48)), (20 + i * 60, 6))
    S.alpha_composite(jo, (1600, y + 164)); label(d, (1600, y + 228), 'overworld at true size (2x): Juno | Kestrel | Larch', F(11))

    y = 374
    for key, info in PANELS.items():
        y = panel(S, d, y, info) + 12
    # ---------------- mocks ----------------
    d.rectangle([10, y, W - 10, y + 440], fill=PANEL)
    d.text((22, y + 8), 'True size: the Desolation-style face window on our maps (Rev 22), and the EBDX battle intro (trainer 160x160, bottom-centre on the foe base)',
           font=FB(15), fill=GOLD)
    fer = demagenta(Image.open(G + 'maps_out/previews/100_Ferrow_s_Landing.png')).crop((1284, 1508, 1796, 1892))
    lab = demagenta(Image.open(G + 'maps_out/previews/103_Larch_Research_Station.png')).crop((96, 96, 608, 480))
    kow = KE.overworld().crop((0, 0, 32, 48)); low = LA.overworld().crop((0, 0, 32, 48))
    m1 = face_window_mock(up(KE.portrait('smug').image(), 2), 'Kestrel', 'You came in on the last ferry? Great.',
                          "Velmora's sinking and they're still letting tourists on.", fer, kow, (330, 150))
    m2 = face_window_mock(up(LA.portrait('deadpan').image(), 2), 'Larch', 'I lit up this whole region, you know.',
                          "And I think I'm killing it. Drink your tea.", lab, low, (300, 150))
    b1 = battle_mock(up(KE.front().image(), 2), 'You are challenged by Rival Kestrel!')
    b2 = battle_mock(up(LA.front().image(), 2), 'Professor Larch wants to battle!')
    for i, m in enumerate((m1, m2, b1, b2)):
        S.alpha_composite(m.resize((512 * 4 // 5, 384 * 4 // 5), Image.NEAREST) if False else m, (22 + i * 540, y + 36))
    label(d, (22, y + 424), 'Kestrel (smug) on Ferrow\'s Landing (map 100) | Larch (deadpan) in the Tidewatch station (map 103) | '
          'battle intros on the MEADOW backdrop, framed like the engine capture in sheet 11', F(11))
    y += 452
    S = S.crop((0, 0, W, y + 10))
    S.convert('RGB').save(OUT, optimize=True)
    print(OUT, S.size)


def panel(S, d, y0, info):
    m = info['mod']; W = S.width; h = info['h']
    d.rectangle([10, y0, W - 10, y0 + h], fill=PANEL)
    d.text((22, y0 + 8), info['title'], font=FB(15), fill=GOLD)
    label(d, (22, y0 + 30), info['concept'], F(12), INK)
    yb = y0 + 54
    label(d, (22, yb), '1  Silhouettes, black at 2x and 1x on cream (guide 2.1). Hook nobody else in the cast has: ' + info['hook'], F(12), INK)
    sil_row(S, d, 22, yb + 20, m)
    # 2 design + palette
    yb += 250
    label(d, (22, yb), '2  Chosen design and colour plan (3 colours + 1 accent; skin, eyes and outline not counted)', F(12), INK)
    fr = m.front().image()
    S.alpha_composite(plate(fr, 2, CREAM), (22, yb + 20))
    S.alpha_composite(plate(fr, 2, FIELD), (196, yb + 20))
    S.alpha_composite(plate(fr, 1, FIELD), (370, yb + 20))
    label(d, (22, yb + 192), 'battle front 2x on cream and on the field, 1x', F(11))
    swatches(d, 470, yb + 24, info['swatches'])
    for i, t in enumerate(info['design']):
        label(d, (470, yb + 30 + len(info['swatches']) * 21 + i * 15), t, F(11))
    # previous version
    xp = 1060
    label(d, (xp, yb + 20), 'previous (what this replaces)', F(11), DIM)
    for i, (f, cap) in enumerate(info['prev']):
        im = kb.load(f)
        if im.width > 100: im = kb.native(im)[0]
        S.alpha_composite(plate(im, 2 if im.width <= 80 else 1, FIELD), (xp + i * 172, yb + 38))
        label(d, (xp + i * 172, yb + 210), cap, F(10))
    # overworld
    xo = 1600
    label(d, (xo, yb), '3  Overworld, 16x24 frames at 3x (rows: down, left, right, up; stand, step, stand, step)', F(12), INK)
    S.alpha_composite(plate(ow_frames_strip(m.overworld(), 3), 1, FIELD, 6), (xo, yb + 20))
    # 4 portraits
    yp = yb + 338
    label(d, (22, yp), '4  Portraits: 48-px art; 2x = the 96x96 file on the window plate, 1x below. One base face; expressions move brows, '
          'lids and mouth only. ' + info['portrait_note'], F(12), INK)
    ex = m.PORTRAIT_EXPRS
    for i, e in enumerate(ex):
        im = m.portrait(e).image()
        x = 22 + i * 108
        S.alpha_composite(plate(im, 2, WIN), (x, yp + 20))
        S.alpha_composite(plate(im, 1, WIN), (x, yp + 128))
        S.alpha_composite(plate(im, 1, CREAM), (x + 54, yp + 128))
        label(d, (x, yp + 184), e, F(11), GOLD if e in info['sig'] else DIM)
    # 5x neutral + checklist
    xz = 22 + len(ex) * 108 + 10
    nim = m.portrait('neutral').image()
    S.alpha_composite(plate(nim, 4, WIN), (xz, yp + 20))
    label(d, (xz, yp + 222), 'neutral at 4x', F(11))
    xc = xz + 210
    for i, t in enumerate(info['checks']):
        label(d, (xc, yp + 20 + i * 15), t, F(11), INK if i == 0 else DIM)
    return y0 + h


PANELS = {}


def build_panels():
    rep = {}
    PANELS['KESTREL'] = dict(
        mod=KE, h=880,
        title='KESTREL VANE - rival, 16. "A boy holding his dead mother\'s coat closed against the wind."',
        concept='Proud, guarded, cutting; a hint of grief (Morwen Vane, Ghost Warden, died in exile). Kept from the user\'s pick A2 (sheet 17): '
                'the collar-up black greatcoat a size too big, crimson lining, side-swept navy fringe, Honedge at his side.',
        hook='the tall greatcoat collar standing round his jaw (tips stick out past the head even at 16 px)',
        swatches=[('1 black wool (coat)', list(KE.COAT)), ('2 navy (hair, trousers)', list(KE.HAIR) + ['181a3c']),
                  ('3 silver-grey (shirt)', list(KE.SHIRT)), ('accent: crimson lining', list(KE.CRIM)),
                  ('skin', list(KE.SK)), ('eyes: steel grey-blue', ['f4f2f6', '7282b8', '2c3260']), ('outline', ['140f1e']),
                  ('prop: Honedge', list(KE.GOLD) + ['a8e4f8'])],
        design=['Black is navy-plum, never grey; the sheen is a cool lavender. Crimson only at the openings: collar,',
                'skirt edges, the split tail (the accent, about 4% of the figure).',
                'Antumbra/Ghost tie (his mother): kept to the story, not the costume - no veil, no purple.',
                'Face kit (guide 2.3): J2 sharp V jaw + E2 almond eyes + B2 strong brows; tired lower lids.',
                'Pose: weight on the back leg, Honedge hanging from the sleeve that hides his right hand,',
                'left hand at the sternum holding the coat closed (his tic), tail flaring behind.'],
        prev=[(G + 'art/work/kitbash/kestrel/KESTREL_A2_native80.png', 'pick A2 (sheet 17)'),
              (G + 'art/out/Graphics/Trainers/RIVAL_KESTREL.png', 'installed v3'),
              (G + 'art/work/kitbash/passes/faces_v1/KESTREL_neutral_48.png', 'faces_v1 (sheet 26)')],
        portrait_note='Signature: smug. Also deadpan, panic, blush, crying (used by the scripts); shocked = surprised (alias file).',
        sig=('smug',),
        checks=['Guide checklist (3.12 / 4 / 5):',
                '- 96x96, 2x2 blocks, alpha 0/255, <= 32 colours, no orphans',
                '- eye line 25, chin 43, whole head in frame, facing right',
                '- silhouette breaks: 2 back tips, temple tip, dip lock, far lock',
                '- jaw J2 / eye E2 / brow B2 - no other main-cast face has it',
                '- hair: 6 locks, 1 arc each, creases in the hair deep tone,',
                '  black only on the silhouette and the hair/skin line',
                '- mouths: line + corners; open = outlined hole, teeth/tongue',
                '- shadows hue-shifted (skin to rose, black to navy-plum)',
                'Who does it look like? Checked: Kieran (fringe over the',
                'eyes + amber eyes - ours keeps both eyes clear, steel-grey),',
                'Hugh (spiky navy, red eyes), Silver, Gladion, N, Grimsley,',
                'Sebastian-style butlers, Reborn/Rejuv/Desolation rivals.',
                'Closest read is "gothic rival"; no single match.'])
    PANELS['LARCH'] = dict(
        mod=LA, h=880,
        title='PROFESSOR IMELDA LARCH - mentor, 56, Tidewatch Station. "The engineer who lit the region and now pours tea at the end of it."',
        concept='Gruff, guilty, kind, deadpan-funny. Kept: grey braid, glasses, the field-scientist coat (pick A, sheet 20: mustard oilskin, the held-out mug). '
                'Changed: the glasses ride on her head (free face for comedy, a break in the hair dome); the flying stole is gone.',
        hook='the reading glasses pushed up on her head + the rope braid over her shoulder',
        swatches=[('1 mustard oilskin (coat)', list(LA.OIL)), ('2 slate knit (sweater, legs)', list(LA.KNIT)),
                  ('3 silver-blue (hair)', list(LA.HAIR) + ['474e6c']), ('accent: coral (readers, rim)', list(LA.CORAL)),
                  ('skin', list(LA.SK)), ('eyes: sea-glass', ['f8f4f0', '4fa294', '1f5a5a']), ('outline', ['1e1418']),
                  ('prop: mug, kelp tea', ['ffffff', 'e8eef4', 'b8c4d6'] + list(LA.TEA))],
        design=['Coastal field scientist, not a lab coat: waxed oilskin, fisherman\'s roll-neck, rubber boots.',
                'Silver hair shaded blue-grey (Dorian\'s is lavender) so the two greys never match.',
                'Face kit: J4 long jaw + E3 hooded eyes + B1 soft mobile brows; crow\'s foot, nasolabial line.',
                'Pose: "Drink your tea." - the mug held out to the player, other fist on her hip.',
                'Comedy: the readers jump off her head when she\'s shocked; "not crying" = two streams.'],
        prev=[(G + 'art/work/kitbash/larch/LARCH_A_native80.png', 'pick A (sheet 20)'),
              (G + 'art/out/Graphics/Trainers/LARCH.png', 'installed front'),
              (G + 'art/out/Graphics/Portraits/LARCH_neutral.png', 'installed portrait')],
        portrait_note='All 10 script expressions + surprised. Signatures: deadpan, crying ("it\'s the tea"), shocked.',
        sig=('deadpan', 'crying', 'shocked'),
        checks=['Guide checklist (3.12 / 4 / 5):',
                '- 96x96, 2x2 blocks, alpha 0/255, <= 32 colours, no orphans',
                '- eye line 23, chin 42, whole head in frame, facing right',
                '- silhouette breaks: the readers, crown wisp, loose far strand,',
                '  the braid over the shoulder',
                '- jaw J4 / eye E3 / brow B1 - unique in the main cast',
                '- mouths: line + corners; open = outlined hole, teeth/tongue',
                '- shadows hue-shifted (skin to rose, silver to blue-grey)',
                'Who does it look like? Checked: Magnolia (bun + cane - ours',
                'has neither), Bertha, Agatha, Juniper/Colress/Fennel (lab',
                'coats), Cheren (red glasses - young man, on the face),',
                'Reborn/Rejuv/Desolation elders. No match.'])


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    build_panels()
    if what in ('export', 'all'):
        import json; print(json.dumps(export(), indent=0, default=str)[:1500])
    if what in ('sheet', 'all'):
        sheet()
