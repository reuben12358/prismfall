"""sheet_cast.py - review sheet for one early-cast battle front: variations (4x, 2x, 1x in battle), official references at
the same density (2x, 1x), Juno's installed front for scale, and a donors strip.
python3 -I tools/kitbash/sheet_cast.py kestrel|dorian|tamsin|larch|edda
Each recipe module exposes: NAME, SHEET, TITLE, VARIANTS [(key, note)], PICK, REFS [(spec, label)], DONORS [(spec, part)],
build(key) -> 80x80 RGBA."""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, show, sheet09 as s
from PIL import Image, ImageDraw

JUNO = kb.GAME + '/art/out/Graphics/Trainers/RIVAL_JUNO.png'


def export(m):
    d = kb.WORK + '/' + m.NAME.lower()
    os.makedirs(d, exist_ok=True)
    outs = {}
    for k, _ in m.VARIANTS:
        im = m.build(k)
        outs[k] = im
        im.save('%s/%s_%s_native80.png' % (d, m.NAME, k))
        kb.up(im, 2).save('%s/%s_%s.png' % (d, m.NAME, k))
    return outs


def donor(spec):
    if spec.startswith('B:') or spec.startswith('I:') or spec.startswith('sd:') or spec.startswith('file:'):
        return s.donor_img(spec) if not spec.startswith('file:') else kb.native(kb.load(spec[5:]))[0]
    return s.donor_img(spec)


def main(name):
    m = importlib.import_module(name)
    outs = export(m)
    n = len(m.VARIANTS)
    W, H = 1960, 1130
    sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh)
    f16, f13, f11, f10 = kb.font(17), kb.font(13), kb.font(11), kb.font(10)
    d.text((16, 10), m.TITLE, font=f13, fill=s.TXT)
    # variations, 4x
    pw = 24 + n * 340
    d.rectangle((16, 36, 16 + pw, 640), fill=s.PANEL)
    d.text((26, 42), 'variations (4x, then 2x and 1x on the battle field)', font=f16, fill=s.ACC)
    for i, (k, note) in enumerate(m.VARIANTS):
        x = 26 + i * 340
        im = outs[k]
        sh.alpha_composite(s.stage(im, 4, s.STAGE, 330, 330), (x, 70))
        sh.alpha_composite(s.stage(im, 2, s.STAGE, 168, 168), (x, 406))
        sh.alpha_composite(s.stage(im, 1, s.BATTLE, 156, 90), (x + 172, 406))
        sh.alpha_composite(s.stage(im, 1, s.STAGE, 156, 74), (x + 172, 500))
        s.wrap(d, ('PICK ' if k == m.PICK else '') + note, (x + 2, 580), 326, f10, s.ACC if k == m.PICK else s.TXT)
    # references
    rx0 = 32 + pw
    d.rectangle((rx0 - 8, 36, W - 16, 640), fill=s.PANEL)
    d.text((rx0, 42), 'references, same density (2x, 1x)', font=f13, fill=s.ACC)
    refs = [(spec, lab) for spec, lab in m.REFS] + [('file:' + JUNO, 'Juno (ours, installed)')]
    cols = max(1, (W - 16 - rx0) // 176)
    for i, (spec, lab) in enumerate(refs):
        im = kb.native(kb.load(spec[5:]))[0] if spec.startswith('file:') else show.get_native(spec)[0]
        x = rx0 + (i % cols) * 176; y = 66 + (i // cols) * 286
        sh.alpha_composite(s.stage(im, 2, s.STAGE, 168, 168), (x, y))
        sh.alpha_composite(s.stage(im, 1, s.BATTLE, 168, 90), (x, y + 172))
        d.text((x + 2, y + 266), lab, font=f10, fill=s.DIM)
    # pick at 1x beside refs at 1x on one strip (the honest comparison)
    y = 652
    d.rectangle((16, y, W - 16, y + 150), fill=s.PANEL)
    d.text((26, y + 6), '1x line-up on the battle field: our variations, then the references', font=f13, fill=s.ACC)
    strip = [outs[k] for k, _ in m.VARIANTS] + [kb.native(kb.load(sp[5:]))[0] if sp.startswith('file:') else show.get_native(sp)[0] for sp, _ in refs]
    bg = Image.new('RGBA', (W - 48, 100), s.BATTLE)
    for i, im in enumerate(strip):
        bg.alpha_composite(im, (8 + i * 86, 18))
    sh.alpha_composite(bg, (32, y + 32))
    # donors
    y = 812
    d.rectangle((16, y, W - 16, H - 12), fill=s.PANEL)
    d.text((26, y + 6), 'donors (native, 2x) and what was taken', font=f13, fill=s.ACC)
    x = 26
    for spec, part in m.DONORS:
        dn = donor(spec)
        if dn.size[0] > 100 or dn.size[1] > 100:
            dn = dn.crop(kb.bbox(dn))
        z = kb.up(dn, 2)
        bgd = Image.new('RGBA', (max(170, z.size[0] + 8), 214), s.STAGE)
        bgd.alpha_composite(z, ((bgd.size[0] - z.size[0]) // 2, 214 - z.size[1] - 4))
        if x + bgd.size[0] > W - 20:
            break
        sh.alpha_composite(bgd, (x, y + 30))
        s.wrap(d, part, (x + 2, y + 248), bgd.size[0] - 4, f10, s.TXT)
        x += bgd.size[0] + 10
    if getattr(m, 'NOTE', ''):
        s.wrap(d, m.NOTE, (26, H - 40), W - 60, f10, s.DIM)
    sh.save(kb.GAME + '/art/previews/' + m.SHEET); print(m.SHEET, sh.size)


if __name__ == '__main__':
    main(sys.argv[1])
