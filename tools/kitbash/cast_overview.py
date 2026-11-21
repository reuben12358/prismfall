"""Cast art overview sheet: every character's battle sprite, overworld and dialogue portraits in one place.
python3 tools/kitbash/cast_overview.py  ->  art/previews/28_cast_overview.png"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A = lambda *p: os.path.join(ROOT, 'art', *p)
OUT_G = A('out', 'Graphics')
KB = A('work', 'kitbash')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f_name = ImageFont.truetype(FONTB, 26)
f_txt = ImageFont.truetype(FONT, 17)
f_cap = ImageFont.truetype(FONT, 15)
f_head = ImageFont.truetype(FONTB, 22)

BG = (34, 36, 44)
PANEL = (46, 49, 60)
CELL = (60, 64, 78)
GREEN = (120, 210, 140)
AMBER = (240, 190, 90)
GREY = (170, 174, 190)
WHITE = (236, 238, 244)


def load(path):
    return Image.open(path).convert('RGBA') if os.path.exists(path) else None


def scale_int(im, target_h):
    k = max(1, target_h // im.height)
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def ow_frame(path):
    im = load(path)
    if im is None:
        return None
    fw, fh = im.width // 4, im.height // 4
    return im.crop((0, 0, fw, fh))


def back_frame(path):
    im = load(path)
    if im is None:
        return None
    return im.crop((0, 0, im.height, im.height))


def kb(char, name):
    return os.path.join(KB, char, name)


def portraits(folder, prefix, exprs):
    out = []
    for e in exprs:
        p = os.path.join(folder, '%s_%s.png' % (prefix, e)) if e else os.path.join(folder, prefix + '.png')
        im = load(p)
        if im is not None:
            out.append((im, e or 'base'))
    return out


P_INST = os.path.join(OUT_G, 'Portraits')
FACES_V1 = os.path.join(KB, 'passes', 'faces_v1')
STYLE = A('research', 'style_test')

# (name, role, status colour, status text, battle list, overworld, portraits list, portrait note)
ROWS = [
    ('Juno Hale', 'rival / Ever-Bloom', GREEN, 'Approved: battle, overworld and portraits (pass 3) in the game',
     [(load(os.path.join(OUT_G, 'Trainers', 'RIVAL_JUNO.png')), 'rival'), (load(os.path.join(OUT_G, 'Trainers', 'LEADER_JUNO.png')), 'Warden')],
     ow_frame(os.path.join(OUT_G, 'Characters', 'JUNO.png')),
     portraits(P_INST, 'JUNO', ['neutral', 'happy', 'sad', 'surprised', 'smug', 'wink']), 'installed'),
    ('Kestrel Vane', 'rival', AMBER, 'Battle: old v3 installed, your pick A2 waits to go in. Portrait v1 held back for a redo',
     [(load(os.path.join(OUT_G, 'Trainers', 'RIVAL_KESTREL.png')), 'installed (old)'), (load(kb('kestrel', 'KESTREL_A2.png')), 'pick A2')],
     ow_frame(os.path.join(OUT_G, 'Characters', 'KESTREL.png')),
     portraits(FACES_V1, 'KESTREL', ['neutral', 'smug', 'angry', 'sad', 'surprised']), 'v1, being redone'),
    ('Professor Larch', 'mentor', GREEN, 'Battle, overworld and portraits in the game; pick A waits to replace the battle sprite',
     [(load(os.path.join(OUT_G, 'Trainers', 'LARCH.png')), 'installed'), (load(kb('larch', 'LARCH_A.png')), 'pick A')],
     ow_frame(os.path.join(OUT_G, 'Characters', 'LARCH.png')),
     portraits(P_INST, 'LARCH', ['neutral', 'happy', 'angry', 'deadpan', 'shocked', 'smug']), 'installed'),
    ('Dorian Pell', 'Gym 1, Normal', AMBER, 'Battle pick S waits to go in. New portrait from the style guide (your call)',
     [(load(kb('dorian', 'DORIAN_S.png')), 'pick S')],
     None,
     [(load(os.path.join(STYLE, 'DORIAN_st.png')), 'knowing'), (load(os.path.join(STYLE, 'DORIAN_st_laugh.png')), 'laugh'),
      (load(os.path.join(STYLE, 'DORIAN_st_surprised.png')), 'surprised')], 'style test'),
    ('Tamsin Loom', 'Gym 2, Bug', AMBER, 'Battle pick A waits to go in. No overworld or portrait yet',
     [(load(kb('tamsin', 'TAMSIN_A.png')), 'pick A'), (load(kb('tamsin', 'TAMSIN_B.png')), 'B')], None, [], ''),
    ('Thistle', 'side character', AMBER, 'Battle pick B waits to go in. No overworld or portrait yet',
     [(load(kb('thistle', 'THISTLE_B.png')), 'pick B'), (load(kb('thistle', 'THISTLE_A.png')), 'A')], None, [], ''),
    ('The Mourner', 'villain', AMBER, 'Battle pick C waits to go in. No overworld or portrait yet',
     [(load(kb('mourner', 'MOURNER_C.png')), 'pick C')], None, [], ''),
    ('Vesper', 'Eevee Octave', GREY, 'Candidates only; pass 3 (singing face, ribbons) still to do',
     [(load(kb('vesper', 'VESPER_%s.png' % c)), c) for c in 'ABCD'], None, [], ''),
    ('Edda', 'mentor', GREY, 'Parked: candidates only',
     [(load(kb('edda', 'EDDA_%s.png' % c)), c) for c in 'ABN'], None, [], ''),
    ('Player A', 'protagonist', AMBER, 'Placeholder look in the game files; the final look is waiting on your direction',
     [(load(os.path.join(OUT_G, 'Trainers', 'PLAYER_A.png')), 'front'), (back_frame(os.path.join(OUT_G, 'Trainers', 'PLAYER_A_back.png')), 'back')],
     ow_frame(os.path.join(OUT_G, 'Characters', 'PLAYER_A.png')),
     portraits(P_INST, 'PLAYER_A', ['neutral', 'happy', 'sad', 'shocked']), 'installed'),
    ('Player B', 'protagonist', AMBER, 'Placeholder look in the game files; the final look is waiting on your direction',
     [(load(os.path.join(OUT_G, 'Trainers', 'PLAYER_B.png')), 'front'), (back_frame(os.path.join(OUT_G, 'Trainers', 'PLAYER_B_back.png')), 'back')],
     ow_frame(os.path.join(OUT_G, 'Characters', 'PLAYER_B.png')),
     portraits(P_INST, 'PLAYER_B', ['neutral', 'happy', 'sad', 'shocked']), 'installed'),
]

ROW_H = 250
PAD = 16
LABEL_W = 300
W = 2200


def draw_cell(sheet, d, x, y, im, cap, h):
    im = scale_int(im, h)
    w = max(im.width, 96)
    d.rectangle([x, y, x + w + 12, y + h + 12], fill=CELL)
    sheet.alpha_composite(im, (x + 6 + (w - im.width) // 2, y + 6 + (h - im.height)))
    d.text((x + 6, y + h + 16), cap, font=f_cap, fill=GREY)
    return x + w + 24


def main():
    H = 90 + len(ROWS) * (ROW_H + PAD)
    sheet = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(sheet)
    d.text((PAD, 18), 'Prismfall cast art: battle sprites | overworld | dialogue portraits', font=f_head, fill=WHITE)
    d.text((PAD, 50), 'Green = approved and in the game.  Amber = picked or drafted, waiting on install or approval.  Grey = candidates only.',
           font=f_txt, fill=GREY)
    y = 90
    for name, role, col, status, battles, ow, ports, pnote in ROWS:
        d.rectangle([PAD, y, W - PAD, y + ROW_H], fill=PANEL)
        d.rectangle([PAD, y, PAD + 6, y + ROW_H], fill=col)
        d.text((PAD + 18, y + 14), name, font=f_name, fill=WHITE)
        d.text((PAD + 18, y + 48), role, font=f_txt, fill=GREY)
        # wrap status
        words, line, ly = status.split(), '', y + 80
        for wd in words:
            if d.textlength(line + ' ' + wd, font=f_cap) > LABEL_W - 30:
                d.text((PAD + 18, ly), line.strip(), font=f_cap, fill=col); ly += 20; line = ''
            line += ' ' + wd
        d.text((PAD + 18, ly), line.strip(), font=f_cap, fill=col)
        x = PAD + LABEL_W
        d.text((x, y + 8), 'BATTLE', font=f_cap, fill=GREY)
        for im, cap in battles:
            if im is not None:
                x = draw_cell(sheet, d, x, y + 30, im, cap, 160)
        x += 10
        d.text((x, y + 8), 'OVERWORLD', font=f_cap, fill=GREY)
        if ow is not None:
            x = draw_cell(sheet, d, x, y + 30, ow, 'walk', 144)
        else:
            d.text((x, y + 90), 'none yet', font=f_txt, fill=GREY); x += 120
        x += 10
        d.text((x, y + 8), 'PORTRAITS' + (' (%s)' % pnote if pnote else ''), font=f_cap, fill=GREY)
        if ports:
            for im, cap in ports:
                if x + 130 > W - PAD:
                    break
                x = draw_cell(sheet, d, x, y + 30, im, cap, 96)
        else:
            d.text((x, y + 90), 'none yet', font=f_txt, fill=GREY)
        y += ROW_H + PAD
    out = A('previews', '28_cast_overview.png')
    sheet.convert('RGB').save(out)
    print(out, sheet.size)


if __name__ == '__main__':
    main()
