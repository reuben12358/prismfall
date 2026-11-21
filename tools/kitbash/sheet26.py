"""sheet26.py - art/previews/26_face_portraits_kestrel_dorian.png: dialogue faces v1 for Kestrel and Dorian.
Juno (installed pass 3) for reference, both new sets at 2x and 1x on a dark face-window backdrop, and two true-size
512x384 dialogue mocks laid out like Essentials/Desolation (128x128 face window directly above the message box,
left-aligned: pbPositionNearMsgWindow(facewindow, msgwindow, :left); 96x96 face inside a 16-px frame).
    python3 -I tools/kitbash/faces_v1.py && python3 -I tools/kitbash/sheet26.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image, ImageDraw, ImageFont

FACES = kb.WORK + '/passes/faces_v1'
JUNO = kb.GAME + '/art/out/Graphics/Portraits/JUNO_neutral.png'
OUT = kb.GAME + '/art/previews/26_face_portraits_kestrel_dorian.png'
GAMEFONT = '/home/claude/ref/ebdx/Fonts/power green.ttf'
BG, PANEL, TXT, DIM, ACC = (40, 42, 50, 255), (58, 61, 72, 255), (232, 232, 236, 255), (170, 174, 186, 255), (240, 200, 120, 255)
WIN_BACK = (38, 42, 60, 255)            # stand-in for the face window's backdrop (transparent pixels show it)
SETS = [('KESTREL', ['neutral', 'smug', 'angry', 'sad', 'surprised'],
         'Kestrel Vane - base face: B2W2 VS Cheren (Leader) face only; hair rebuilt as a side-swept fringe with the long lock '
         'over his right eye, steel-grey eyes, collar-up greatcoat with crimson lining (sheet 17, pick A2). '
         'KESTREL_happy.png = the smug face.'),
        ('DORIAN', ['neutral', 'happy', 'smug', 'angry', 'surprised'],
         'Dorian Pell - base face: B2W2 VS Hilbert face only (cap and hair gone); silver swept-back pompadour with the matinee '
         'flick, hazel eyes, pencil moustache, plum velvet collar, white silk ascot, red rose (sheet 18, pick S).')]


def face(name, e):
    return Image.open('%s/%s_%s.png' % (FACES, name, e)).convert('RGBA')


def on_back(im96):
    bg = Image.new('RGBA', im96.size, WIN_BACK); bg.alpha_composite(im96); return bg


def window(d, box, r=6):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, r, fill=(72, 72, 88, 255))
    d.rounded_rectangle((x0 + 2, y0 + 2, x1 - 2, y1 - 2), r - 2, fill=(248, 248, 248, 255))
    d.rounded_rectangle((x0 + 4, y0 + 4, x1 - 4, y1 - 4), r - 3, outline=(208, 208, 224, 255))


def mock(bg_path, crop, name, expr, lines):
    scr = Image.open(bg_path).convert('RGBA').crop(crop)
    d = ImageDraw.Draw(scr)
    window(d, (0, 288, 511, 383))                       # message box, 512x96 at the bottom
    window(d, (0, 160, 127, 287))                       # face window, 128x128 right above it, left-aligned
    scr.alpha_composite(on_back(face(name, expr)), (16, 176))
    d.rectangle((15, 175, 112, 272), outline=(72, 72, 88, 255))
    f = ImageFont.truetype(GAMEFONT, 27)
    for i, t in enumerate(lines):
        d.text((24 + 1, 300 + i * 32 + 1), t, font=f, fill=(168, 184, 184, 255))
        d.text((24, 300 + i * 32), t, font=f, fill=(80, 80, 88, 255))
    d.polygon([(488, 364), (500, 364), (494, 371)], fill=(224, 8, 8, 255))      # continue arrow
    return scr


def main():
    W, H = 1316, 1158
    sh = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
    d.text((16, 10), 'Dialogue faces v1 - KESTREL and DORIAN. 48-px art exported 96x96, Juno pass-3 geometry (eyes from y24, '
                     'mouth y37-39, crown outline at y2), black 1-px outline, Juno\'s skin and mouth ramps, transparent where '
                     'nothing is drawn.', font=f10, fill=TXT)
    d.text((16, 24), 'One base face per character; expressions only move brow / eye / mouth pixels. Files: '
                     'art/work/kitbash/passes/faces_v1/ (not installed). Shown on a dark stand-in for the face window backdrop. '
                     'Recipe: tools/kitbash/faces_v1.py.', font=f10, fill=DIM)
    y = 44
    for name, exprs, note in SETS:
        d.rectangle((16, y, W - 16, y + 340), fill=PANEL)
        d.text((24, y + 4), note, font=f10, fill=ACC)
        ref = on_back(Image.open(JUNO).convert('RGBA'))
        sh.alpha_composite(kb.up(ref, 2), (24, y + 24)); sh.alpha_composite(ref, (24, y + 224))
        d.text((24, y + 324), 'JUNO neutral (installed)', font=f10, fill=DIM)
        d.line((228, y + 24, 228, y + 334), fill=(90, 94, 108, 255), width=2)
        for i, e in enumerate(exprs):
            im = on_back(face(name, e)); x = 240 + i * 212
            sh.alpha_composite(kb.up(im, 2), (x, y + 24)); sh.alpha_composite(im, (x, y + 224))
            d.text((x, y + 324), '%s_%s  (2x, 1x)' % (name, e), font=f10, fill=TXT)
        y += 350
    d.rectangle((16, y, W - 16, y + 412), fill=PANEL)
    d.text((24, y + 4), 'In-game mock, true size (512x384): Essentials face window (128x128, 96x96 face) above the message box, '
                        'left-aligned as in Desolation. Font: Power Green 27. Backgrounds: our map previews.', font=f10, fill=ACC)
    a = mock(kb.GAME + '/maps_out/previews/154_Pell_Playhouse___Auditorium.png', (144, 40, 656, 424), 'DORIAN', 'happy',
             ['Enter, stage left, a stranger!', 'No -- a challenger.'])
    b = mock(kb.GAME + '/maps_out/previews/100_Ferrow_s_Landing.png', (1284, 1508, 1796, 1892), 'KESTREL', 'smug',
             ['Clearly it has awful taste.', 'It picked me.'])
    sh.alpha_composite(a, (24, y + 22)); sh.alpha_composite(b, (24 + 512 + 24, y + 22))
    d.text((24 + 2 * 536, y + 30), 'Dorian (happy): his Ch2 line,\n20_SCRIPT_CH0-2.md, on his own\nstage (map 154).\n\n'
                                    'Kestrel (smug): his line from\nTRIALS_QUESTS.md, on the\nFerrow\'s Landing ferry (map 100).',
           font=f10, fill=DIM)
    sh.save(OUT); print(OUT, sh.size)


if __name__ == '__main__':
    main()
