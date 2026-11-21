"""player2_sheet.py - exports the PLAYER_A / PLAYER_B redo (v2) and renders art/previews/29_redo_player.png.
Exports (nothing is installed): art/work/redo_v2/PLAYER_X/Graphics/{Trainers,Characters,Portraits}/ in the install layout,
plus the alternate colour scheme in art/work/redo_v2/PLAYER_X/alt_ash/Graphics/...
python3 -I art/research/scripts/player2_sheet.py"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
from p2kit import up, black, lint, hx
import player2_palette as P
import player2_portrait as pp
import player2_front as pf
import player2_back as pb
import player2_ow as po
import player2_design as pd

G = '/home/claude/fangame/'
OUT = G + 'art/previews/29_redo_player.png'
WORK = G + 'art/work/redo_v2/'
F = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', n)
FB = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', n)
GAMEF = '/home/claude/ref/ebdx/Fonts/power green narrow.ttf'
BG, PANEL, INK, DIM, GOLD = (30, 30, 38, 255), (44, 44, 54, 255), (236, 236, 240, 255), (176, 176, 190, 255), (244, 208, 120, 255)
CREAM, WIN, GREY, GRASS = (232, 226, 212, 255), (52, 56, 74, 255), (150, 160, 170, 255), (120, 168, 96, 255)
PORTRAIT_SET = pp.EXPRS + []          # + the signature, per character
NAMES = {'A': 'PLAYER_A ("Style A", the boy)', 'B': 'PLAYER_B ("Style B", the girl)'}


def plate(im, k, bg, pad=4):
    b = Image.new('RGBA', (im.width * k + pad * 2, im.height * k + pad * 2), bg)
    b.alpha_composite(up(im, k), (pad, pad)); return b


def lab(d, xy, t, f=None, fill=DIM):
    d.text(xy, t, font=f or F(12), fill=fill)


# ------------------------------------------------------------------------------------------------ export
def export(ch, scheme):
    base = WORK + 'PLAYER_%s/' % ch + ('' if scheme == 'main' else 'alt_%s/' % scheme) + 'Graphics/'
    for sub in ('Trainers', 'Characters', 'Portraits', 'native'):
        os.makedirs(base + sub, exist_ok=True)
    n = 'PLAYER_%s' % ch
    front = pf.build(ch, scheme).image()
    front.save(base + 'native/%s_native80.png' % n); up(front, 2).save(base + 'Trainers/%s.png' % n)
    strip, frames = pb.strip(ch, scheme)
    strip.save(base + 'native/%s_back_native.png' % n); up(strip, 2).save(base + 'Trainers/%s_back.png' % n)
    ow = po.sheet(ch, scheme)
    ow.save(base + 'native/%s_ow_native.png' % n)
    up(ow, 2).save(base + 'Characters/%s.png' % n); up(ow, 2).save(base + 'Characters/trainer_%s.png' % n)
    faces = {}
    for e in pp.EXPRS + [pp.SIGNATURE[ch]]:
        im = pp.build(ch, e, scheme).image(); faces[e] = im
        im.save(base + 'native/%s_%s_48.png' % (n, e)); up(im, 2).save(base + 'Portraits/%s_%s.png' % (n, e))
    up(faces['neutral'], 2).save(base + 'Portraits/%s.png' % n)
    return {'front': front, 'back': strip, 'backs': frames, 'ow': ow, 'faces': faces}


# ------------------------------------------------------------------------------------------------ mocks
def face_window_mock(portrait96, name, line1, line2, bgimg):
    W, H = 512, 384
    m = Image.new('RGBA', (W, H), (70, 90, 120, 255))
    if bgimg is not None: m.alpha_composite(bgimg)
    d = ImageDraw.Draw(m)
    d.rectangle([8, 188, 136, 316], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=3)
    d.rectangle([16, 196, 128, 308], fill=WIN)
    m.alpha_composite(portrait96, (24, 204))
    d.rectangle([8, 320, 504, 378], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=3)
    try: gf = ImageFont.truetype(GAMEF, 24); nf = ImageFont.truetype(GAMEF, 20)
    except Exception: gf = nf = F(16)
    d.text((22, 324), line1, font=gf, fill=(72, 72, 80, 255)); d.text((22, 349), line2, font=gf, fill=(72, 72, 80, 255))
    d.rectangle([8, 158, 8 + 14 + int(d.textlength(name, font=nf)), 184], fill=(248, 248, 248, 255), outline=(40, 40, 52, 255), width=2)
    d.text((15, 160), name, font=nf, fill=(56, 90, 160, 255))
    return m


def battle_mock(back_frame80, line):
    """stock EBDX field backdrop + bases; Juno's installed front on the foe base, our back (frame 0, file size) at x=40 on the
    player's base, message box. A layout mock, not an engine capture."""
    W, H = 512, 384
    BB = '/home/claude/ref/ebdx/Graphics/Battlebacks/'
    m = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    bg = Image.open(BB + 'field_bg.png').convert('RGBA'); m.alpha_composite(bg, (0, 0))
    b1 = Image.open(BB + 'field_base1.png').convert('RGBA'); m.alpha_composite(b1, (256, 112))
    b0 = Image.open(BB + 'field_base0.png').convert('RGBA'); m.alpha_composite(b0, (0, 224))
    j = Image.open(G + 'art/out/Graphics/Trainers/RIVAL_JUNO.png').convert('RGBA')
    m.alpha_composite(j, (384 - 80, 112 + 64 - 160 + 16))
    bf = up(back_frame80, 2)
    m.alpha_composite(bf, (40, 288 - 160 + 8))
    d = ImageDraw.Draw(m)
    d.rectangle([0, 288, 512, 384], fill=(40, 44, 56, 255))
    d.rectangle([12, 298, 500, 374], fill=(248, 248, 248, 255), outline=(90, 96, 120, 255), width=3)
    try: gf = ImageFont.truetype(GAMEF, 24)
    except Exception: gf = F(16)
    d.text((28, 304), line, font=gf, fill=(72, 72, 80, 255))
    return m


def scene(f, box):
    p = G + 'maps_out/previews/' + f
    return Image.open(p).convert('RGBA').crop(box) if os.path.exists(p) else None


# ------------------------------------------------------------------------------------------------ text
DESIGN = {
 'A': ['Concept: "off the last ferry" (kept from the earlier pick): everything he owns is in one canvas sea bag.',
       'Hook: the faded-teal sailcloth BUCKET HAT (brim droops at both ends) + the duffel slung over his left shoulder.',
       'Outfit language (shared with B): cream sailcloth deck jacket, sleeves pushed up, hood rolled at the collar;',
       'slate tee and rolled-cuff trousers; leather deck boots (they reuse the hair ramp: no extra colours).',
       'Harbour motif, lightly: sailcloth, a rope drawstring, the yellow ferry ticket tag on the bag. No anchors.',
       'Face kit: J1 round jaw, E1 big round eyes (flat lash, outer flick), B2 strong brows. Signature: determined.',
       'Pose: weight on the near leg, bag rope in the far fist, ball held out low.'],
 'B': ['Concept: the same kid, the same ferry: B wears the same deck kit, cropped, over shorts and cream knee socks.',
       'Hook: a HIGH SIDE TAIL on her right, tied with a teal sailcloth bow, arcing clear of the head (air between).',
       'The bag rides at her hip on a rope sling across the chest (her diagonal; his is the shoulder sling).',
       'Left-handed: the ball goes up in her left hand on the front, and she throws left-handed on the back sprite,',
       'so the throwing arm never fights the tail. Plum-brown hair (from the v3 PLAYER_B idea), not auburn (Juno).',
       'Face kit: J2 soft V chin, E1 eyes with an upturned lash flick, B1 soft 1-row brows. Signature: grin.',
       'Pose: mid-step, ball raised by the shoulder, the tail swinging out behind.'],
}
SIL_NOTES = {
 'A': {'A1': 'PICK: hat brim + bag read at 1x; no one in the cast wears a bucket hat', 'A2': 'knit watch cap = Edda\'s hook',
       'A3': 'swept spikes read shonen', 'A4': 'hood reads Hollow (Thistle)', 'A5': 'streaming scarf = shonen hero',
       'A6': 'backward cap reads Ash', 'A7': 'goggles = Ossaria/Zenith cue', 'A8': 'sou\'wester too literal'},
 'B': {'B1': 'bucket hat is A\'s', 'B2': 'braid = Larch\'s hook', 'B3': 'PICK: side tail, clear of the head',
       'B4': 'wind-blown: no stable shape', 'B5': 'top bow + long hair: generic', 'B6': 'hood up reads Hollow',
       'B7': 'twin tails read Rosa', 'B8': 'side bunches read May'},
}
WHO = {
 'A': 'Who does it look like? Checked: Red, Ethan, Brendan, Lucas, Hilbert, Nate, Calem, Elio, Victor, Florian (all caps/hats '
      'of other shapes); Gilligan (white hat, red shirt) and Ness (red cap): no. Edda (red watch cap): different headwear. No match.',
 'B': 'Who does it look like? Checked: Misty (short orange side tail), Hilda, Rosa, Lyra, Kris, Lisia, Serena, May, Dawn, Juliana; '
      'Katniss/Elsa (side braids - why it is a tail, not a braid). Plum hair + teal bow + cream jacket: no match.',
}
CHECK = ['Portraits: 96x96, 2x2 blocks, alpha 0/255, eye line 27, chin 41-42, head in frame, faces right, >= 2 px air at right',
         'Hooks visible in black (hat brim + bag / side tail + bow); >= 3 silhouette breaks each',
         'Hair: clumps with one arc each, creases in the darkest hair tone, black only on boundaries',
         'Mouths: closed = line + corners; open = outlined hole + dark interior + teeth / tongue rows',
         '3 colours + 1 accent: cream 60 / slate 30 / teal 10 + ferry-ticket yellow; shadows hue-shifted (cream -> lavender)',
         'Expressions change only brows, eyes, mouth and marks (tears, sweat drop, blush hatch)']


def palette_strip(d, x, y, sc):
    rows = [('1 sailcloth cream', sc['cream']), ('2 deep-sea slate', sc['slate']), ('3 prism teal', sc['teal']),
            ('accent: ferry ticket', sc['yel']), ('hair', sc['hair'][:5]), ('skin', P.SKIN), ('eyes', sc['iris'] + (P.EYE_W,)),
            ('outline', (P.K,))]
    for i, (n, cols) in enumerate(rows):
        yy = y + i * 20
        lab(d, (x, yy + 3), n, F(11), INK)
        for j, c in enumerate(cols):
            d.rectangle([x + 126 + j * 19, yy, x + 142 + j * 19, yy + 16], fill=hx(c), outline=(0, 0, 0, 255))


# ------------------------------------------------------------------------------------------------ sheet
def main():
    art = {(c, s): export(c, s) for c in 'AB' for s in ('main', 'ash')}
    W, H = 1900, 4300
    S = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(S)
    d.text((16, 10), 'SHEET 29 - Player redo v2: PLAYER_A and PLAYER_B, original construction (designed shapes, no donor pixels)',
           font=FB(18), fill=INK)
    lab(d, (16, 36), 'Nothing installed. Exports in art/work/redo_v2/PLAYER_A|B/Graphics/{Trainers,Characters,Portraits} (install layout) and '
                     '.../alt_ash/. Recipes: art/research/scripts/player2_*.py. Guide: art/STYLE_GUIDE.md.')
    # ---- Juno reference
    y = 62
    d.rectangle([10, y, W - 10, y + 250], fill=PANEL)
    d.text((22, y + 8), 'REFERENCE - Juno (approved anchor, installed): battle 2x (file size), overworld 3x, portraits 2x and 1x',
           font=FB(14), fill=GOLD)
    jf = Image.open(G + 'art/out/Graphics/Trainers/RIVAL_JUNO.png').convert('RGBA')
    S.alpha_composite(plate(jf.resize((80, 80), Image.NEAREST), 2, GREY), (22, y + 34))
    jo = Image.open(G + 'art/out/Graphics/Characters/JUNO.png').convert('RGBA').resize((64, 96), Image.NEAREST)
    S.alpha_composite(plate(jo.crop((0, 0, 64, 24)), 3, GREY), (200, y + 34))
    S.alpha_composite(plate(jo.crop((0, 72, 64, 96)), 3, GREY), (200, y + 120))
    x = 410
    for e in ('neutral', 'happy', 'sad', 'surprised', 'wink'):
        jp = Image.open(G + 'art/out/Graphics/Portraits/JUNO_%s.png' % e).convert('RGBA')
        S.alpha_composite(plate(jp, 1, WIN), (x, y + 34)); lab(d, (x, y + 142), e, F(11))
        S.alpha_composite(plate(jp.resize((48, 48), Image.NEAREST), 1, WIN), (x, y + 160)); x += 112
    # 1x line-up on grass: Juno + A + B fronts, and the walkers
    g = Image.new('RGBA', (360, 200), GRASS)
    g.alpha_composite(jf.resize((80, 80), Image.NEAREST), (10, 10)); g.alpha_composite(art[('A', 'main')]['front'], (100, 10))
    g.alpha_composite(art[('B', 'main')]['front'], (190, 10))
    g.alpha_composite(jo.crop((0, 0, 16, 24)), (40, 120)); g.alpha_composite(art[('A', 'main')]['ow'].crop((0, 0, 16, 24)), (130, 120))
    g.alpha_composite(art[('B', 'main')]['ow'].crop((0, 0, 16, 24)), (220, 120))
    g2 = up(g, 2).crop((0, 0, 720, 400))
    S.alpha_composite(g, (1000, y + 34)); lab(d, (1000, y + 238), '1x on grass: Juno | A | B (fronts and walkers)', F(11))
    S.alpha_composite(up(g.crop((0, 0, 270, 110)), 2).crop((0, 0, 520, 220)), (1370, y + 24))
    lab(d, (1370, y + 238), '2x (in-game front size): Juno | A | B', F(11))

    y += 262
    for ch in 'AB':
        y = character_panel(S, d, y, ch, art)
    # ---- mocks
    d.rectangle([10, y, W - 10, y + 860], fill=PANEL)
    d.text((22, y + 8), 'TRUE SIZE: Desolation-style face window (Rev 22) on our maps, and a battle-scene layout mock (stock EBDX field '
                        'backdrop, Juno\'s installed front, our back sprite frame 0)', font=FB(14), fill=GOLD)
    fa, fb_ = art[('A', 'main')]['faces'], art[('B', 'main')]['faces']
    m1 = face_window_mock(up(fa['neutral'], 2), 'You', 'Professor Larch? I came on the last ferry.', 'Mum said to find you.',
                          scene('100_Ferrow_s_Landing.png', (1284, 1508, 1796, 1892)))
    m2 = face_window_mock(up(fb_['grin'], 2), 'You', "Scanned? Fine. Scan me again -", "I'm still going to Crownhaven.",
                          scene('100_Ferrow_s_Landing.png', (1536, 768, 2048, 1152)))
    m3 = face_window_mock(up(fa['shocked'], 2), 'You', '...NULL? What does that', 'mean, NULL?', scene('100_Ferrow_s_Landing.png', (128, 1536, 640, 1920)))
    # the walkers at true in-game size (2x art) on the same maps
    m1.alpha_composite(up(art[('A', 'main')]['ow'].crop((16, 24, 32, 48)), 2), (300, 236))
    m2.alpha_composite(up(art[('B', 'main')]['ow'].crop((0, 0, 16, 24)), 2), (300, 240))
    m3.alpha_composite(up(art[('A', 'ash')]['ow'].crop((0, 72, 16, 96)), 2), (420, 150)) if False else None
    S.alpha_composite(m1, (22, y + 36)); S.alpha_composite(m2, (22 + 530, y + 36)); S.alpha_composite(m3, (22 + 1060, y + 36))
    b1 = battle_mock(art[('A', 'main')]['backs'][0], 'Rival Juno sent out Bounsweet!')
    b2 = battle_mock(art[('B', 'main')]['backs'][0], 'Go! ...')
    b3 = battle_mock(art[('B', 'main')]['backs'][3], '(throw frame 3)')
    S.alpha_composite(b1, (22, y + 440)); S.alpha_composite(b2, (22 + 530, y + 440)); S.alpha_composite(b3, (22 + 1060, y + 440))
    y += 872
    # checklist
    d.rectangle([10, y, W - 10, y + 150], fill=PANEL)
    d.text((22, y + 8), 'CHECKLIST (guide 3.12 / 4 / 5) - self-review against Juno at 1x and zoomed', font=FB(14), fill=GOLD)
    for i, t in enumerate(CHECK):
        lab(d, (22, y + 32 + i * 18), '[x] ' + t, F(12), INK)
    y += 162
    S = S.crop((0, 0, W, y + 10))
    S.convert('RGB').save(OUT, optimize=True)
    print(OUT, S.size)
    return art


def character_panel(S, d, y, ch, art):
    W = S.width
    a = art[(ch, 'main')]; alt = art[(ch, 'ash')]; sc = P.SCHEMES[ch]['main']
    top = y
    d.rectangle([10, y, W - 10, y + 1290], fill=PANEL)
    d.text((22, y + 8), NAMES[ch], font=FB(16), fill=GOLD)
    # 1 silhouettes
    lab(d, (22, y + 34), '1  Silhouettes (true front size, black; then 2x): one body, eight head/prop ideas. Pick and one-line reasons:')
    x = 22
    for n, im in pd.thumbs(ch).items():
        k = n.split()[0]
        pick = 'PICK' in SIL_NOTES[ch][k]
        S.alpha_composite(plate(im, 1, CREAM, 2), (x, y + 54))
        S.alpha_composite(plate(im.crop((10, 0, 70, 80)), 2, CREAM, 2), (x + 86, y + 54))
        lab(d, (x, y + 220), n, F(10), GOLD if pick else DIM)
        lab(d, (x, y + 234), SIL_NOTES[ch][k][:38], F(9), GOLD if pick else DIM)
        x += 232
    # the final silhouette
    lab(d, (22, y + 254), 'final:', F(11), GOLD)
    S.alpha_composite(plate(black(a['front']), 1, CREAM, 2), (70, y + 252))
    S.alpha_composite(plate(black(a['backs'][0]), 1, CREAM, 2), (156, y + 252))
    S.alpha_composite(plate(black(a['ow'].crop((0, 0, 16, 24))), 2, CREAM, 2), (242, y + 252))
    S.alpha_composite(plate(black(a['faces']['neutral']), 1, CREAM, 2), (282, y + 252))
    # 2 chosen design
    yb = y + 346
    lab(d, (22, yb), '2  Chosen design (front, 3x) and colour plan: 3 colours + 1 accent')
    S.alpha_composite(plate(a['front'], 3, CREAM), (22, yb + 20))
    palette_strip(d, 280, yb + 24, sc)
    for i, t in enumerate(DESIGN[ch]):
        lab(d, (560, yb + 24 + i * 17), t, F(11), INK if i == 0 else DIM)
    lb = lint(a['front'])
    lab(d, (560, yb + 24 + 7 * 17 + 6), 'front: %d colours (cap 36), %d semi-transparent px, %d orphans; walker sheet: %d colours (cap 24)'
        % (lb['colours'], lb['semi'], len(lb['orphans']), lint(a['ow'])['colours']), F(11), DIM)
    lab(d, (560, yb + 24 + 8 * 17 + 6), WHO[ch][:150], F(11), DIM)
    lab(d, (560, yb + 24 + 9 * 17 + 6), WHO[ch][150:], F(11), DIM)
    # 3 battle 2x + back strip
    yc = yb + 280
    lab(d, (22, yc), '3  Battle front at 2x (file size, 160x160) and 1x; EBDX back strip (800x160, 5 frames: idle, wind-up, cocked, throw, throw)')
    S.alpha_composite(plate(up(a['front'], 2), 1, GREY), (22, yc + 20))
    S.alpha_composite(plate(a['front'], 1, GRASS), (196, yc + 20))
    S.alpha_composite(plate(up(a['back'], 2), 1, GREY), (290, yc + 20))
    lab(d, (290, yc + 188), 'back frames at file size; frame 4 = frame 3, as in the installed PLAYER_A_back.png', F(11))
    # 4 overworld 3x + portraits
    yd = yc + 212
    lab(d, (22, yd), '4  Overworld 3x (rows: down, left, right, up; cols: stand, step, stand, step)')
    S.alpha_composite(plate(a['ow'], 3, GREY), (22, yd + 20))
    lab(d, (230, yd + 20), '1x:', F(11)); S.alpha_composite(plate(a['ow'], 1, GRASS), (230, yd + 36))
    # portraits
    xp = 330
    lab(d, (xp + 520, yd), '5  Portraits, 96x96 (2x) on the window plate, 48 (1x), 96 on cream. Script set + surprised + signature:')
    names = pp.EXPRS + [pp.SIGNATURE[ch]]
    for i, e in enumerate(names):
        px = xp + (i % 6) * 252; py = yd + 20 + (i // 6) * 150
        S.alpha_composite(plate(up(a['faces'][e], 2), 1, WIN, 2), (px, py))
        S.alpha_composite(plate(a['faces'][e], 1, WIN, 2), (px + 104, py))
        S.alpha_composite(plate(up(a['faces'][e], 2), 1, CREAM, 2), (px + 156, py))
        lab(d, (px, py + 102), e + ('  (signature)' if e == pp.SIGNATURE[ch] else ''), F(11), GOLD if e == pp.SIGNATURE[ch] else DIM)
    # 6 alternate scheme strip
    ye = yd + 330
    lab(d, (22, ye), '6  Alternate colour scheme ("ash": the colourless look once floated - ash hair, chalk white, grey-violet, the old '
                     'red ferry tag). Same art, region recolour. For the user to choose.', F(12), INK)
    S.alpha_composite(plate(up(alt['front'], 2), 1, GREY), (22, ye + 20))
    S.alpha_composite(plate(up(alt['backs'][0], 2), 1, GREY), (196, ye + 20))
    S.alpha_composite(plate(alt['ow'].crop((0, 0, 64, 24)), 3, GREY), (370, ye + 20))
    S.alpha_composite(plate(alt['ow'].crop((0, 72, 64, 96)), 3, GREY), (370, ye + 104))
    for i, e in enumerate(('neutral', 'happy', 'surprised', pp.SIGNATURE[ch])):
        S.alpha_composite(plate(up(alt['faces'][e], 2), 1, WIN, 2), (580 + i * 108, ye + 20))
    S.alpha_composite(plate(up(a['faces']['neutral'], 2), 1, WIN, 2), (580 + 4 * 108 + 20, ye + 20))
    lab(d, (580 + 4 * 108 + 20, ye + 124), 'main, for comparison', F(11))
    return top + 1302


if __name__ == '__main__':
    main()
