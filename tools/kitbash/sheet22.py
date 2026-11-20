"""sheet22.py - the player review sheet art/previews/22_player.png + exports to art/work/kitbash/player/.
Fronts (player.py), EBDX backs (player_back.py), overworld charsets (player_ow.py). Nothing is installed except the two
overworld sheets, into the preview-only folder art/out/preview_only/Graphics/Characters/.
python3 -I tools/kitbash/sheet22.py"""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, show, mat, sheet09 as s, player as pl, player_back as pb, player_ow as po, backstrips as bs
from PIL import Image, ImageDraw

D = kb.WORK + '/player'
JUNO = kb.GAME + '/art/out/Graphics/Trainers/RIVAL_JUNO.png'
FRONTS = [('A1', 'PICK A1 (Style A): "off the last ferry". Rubbing the back of his head, a little lost on the quay; ash hair, '
                 'chalk-white jacket over a slate tee, teal trim, the faded teal sea bag over one shoulder with a red ferry tag. '
                 'Backpacker body (pack -> sea bag), acetrainer-gen6 head.'),
          ('A2', 'A2: the same kid in the snow-ace battle stance, ball low, teal scarf, bag on his back. Pairs with B1.'),
          ('B1', 'PICK B1 (Style B): long ash hair blown sideways, teal scarf, white jacket, grey gloves, slate, boots; '
                 'the sea bag on her back. Ace Trainer (snow) body, recoloured and re-dressed.'),
          ('B2', 'B2: "hello, I\'m new here", waving under a white cap with a teal band; the pack becomes the sea bag. '
                 'Hiker (gen 9) body.')]
REFS = [('sd:hilbert', 'Hilbert (official BW)'), ('sd:hilda', 'Hilda (official BW)'), ('sd:nate', 'Nate (official B2W2)'),
        ('sd:rosa', 'Rosa (official B2W2)')]
DONORS = [('sd:backpacker', 'backpacker: A1 body, pose, pack -> sea bag'), ('sd:acetrainer-gen6', 'acetrainer-gen6: A1/A2 head'),
          ('sd:acetrainersnowf', 'acetrainersnowf: B1 body'), ('sd:acetrainersnow', 'acetrainersnow: A2 body'),
          ('sd:hiker-gen9', 'hiker-gen9: B2 body'),
          ('file:/home/claude/ref/ebdx/Graphics/Trainers/POKEMONTRAINER_Red_back.png', 'Red big back (base project): A back body + throw'),
          ('file:/home/claude/ref/ebdx/Graphics/Trainers/POKEMONTRAINER_Leaf_back.png', 'Leaf big back: B back body + throw'),
          ('file:/home/claude/ref/games/rejuvenation/Graphics/Characters/trback001.png', 'Rejuv trback001: A back head + scarf'),
          ('file:/home/claude/ref/games/rejuvenation/Graphics/Characters/trback002.png', 'Rejuv trback002: B back hair crown'),
          ('file:/home/claude/ref/ebdx_renovation/Graphics/Characters/trainer_COOLTRAINER_M.png', 'charsets: COOLTRAINER_M hair + Red body (A), BEAUTY hair + Leaf body (B)')]


def export():
    os.makedirs(D, exist_ok=True)
    fr = {}
    for k, _ in FRONTS:
        im = pl.build(k); fr[k] = im
        name = 'PLAYER_%s_%s' % (k[0], k)
        im.save('%s/%s_native80.png' % (D, name)); kb.up(im, 2).save('%s/%s.png' % (D, name))
    backs = {'A': pb.back_a(), 'B': pb.back_b()}
    for k, frs in backs.items():
        st = pb.strip(frs, 2)
        st.save('%s/PLAYER_%s_back.png' % (D, k))
    po.main()
    pv = kb.GAME + '/art/out/preview_only/Graphics/Characters'
    os.makedirs(pv, exist_ok=True)
    for k in 'AB':
        shutil.copy('%s/PLAYER_%s_ow.png' % (D, k), '%s/trainer_PLAYER_%s.png' % (pv, k))
        shutil.copy('%s/PLAYER_%s_ow.png' % (D, k), '%s/PLAYER_%s.png' % (pv, k))
    return fr, backs


def battle_mock(back_frame, front_file, w=512, h=384):
    """EBDX-like placement: backsprite frame at file size, x=40, bottom at screen bottom +20 (Y_OFFSET -20 lifts it);
    opponent front at file size, bottom-centre near (370, 200)."""
    bg = Image.new('RGBA', (w, h), (120, 156, 108, 255)); d = ImageDraw.Draw(bg)
    d.rectangle((0, 0, w, 150), fill=(150, 184, 206, 255))
    d.ellipse((290, 170, 450, 215), fill=(98, 136, 90, 255))
    d.ellipse((10, 330, 250, 400), fill=(98, 136, 90, 255))
    if front_file:
        fr = Image.open(front_file).convert('RGBA')
        bg.alpha_composite(fr, (370 - fr.size[0] // 2, 200 - fr.size[1]))
    bf = kb.up(back_frame, 2)
    y = h - bf.size[1] + 20 - 20
    bg.alpha_composite(bf, (40, max(0, y)) if y >= 0 else (40, 0))
    return bg


def main():
    fronts, backs = export()
    W, Hh = 1960, 2210
    sh = Image.new('RGBA', (W, Hh), s.BG); d = ImageDraw.Draw(sh)
    f16, f13, f10 = kb.font(17), kb.font(13), kb.font(10)
    d.text((16, 10), 'PLAYER (PLAYER_A "Style A", PLAYER_B "Style B"): "OFF THE LAST FERRY". The kid who owns exactly one bag: '
                     'colourless (chalk white, ash, slate) with one accent, the faded prism-teal sea bag with a red ferry tag. '
                     'Fronts 80-px art (file 160x160); EBDX backs in the base project\'s player format (5 frames of 160x234); '
                     'charsets 16x24 (file 128x192).', font=f10, fill=s.TXT)
    # ---- fronts
    pw = 24 + 4 * 300
    d.rectangle((16, 32, 16 + pw, 610), fill=s.PANEL)
    d.text((26, 38), 'fronts (4x, then 2x and 1x on the battle field)', font=f16, fill=s.ACC)
    for i, (k, note) in enumerate(FRONTS):
        x = 26 + i * 300; im = fronts[k]
        sh.alpha_composite(s.stage(im, 3, s.STAGE, 290, 250), (x, 64))
        sh.alpha_composite(s.stage(im, 2, s.STAGE, 168, 168), (x, 318))
        sh.alpha_composite(s.stage(im, 1, s.BATTLE, 118, 86), (x + 172, 318))
        sh.alpha_composite(s.stage(im, 1, s.STAGE, 118, 78), (x + 172, 408))
        s.wrap(d, note, (x + 2, 492), 290, f10, s.ACC if note.startswith('PICK') else s.TXT)
    # ---- references
    rx0 = 32 + pw
    d.rectangle((rx0 - 8, 32, W - 16, 610), fill=s.PANEL)
    d.text((rx0, 38), 'official players, same density (2x, 1x)', font=f13, fill=s.ACC)
    refs = REFS + [('file:' + JUNO, 'Juno (ours, installed)')]
    for i, (spec, lab) in enumerate(refs):
        im = kb.native(kb.load(spec[5:]))[0] if spec.startswith('file:') else show.get_native(spec)[0]
        x = rx0 + (i % 4) * 172; y = 60 + (i // 4) * 276
        sh.alpha_composite(s.stage(im, 2, s.STAGE, 166, 166), (x, y))
        sh.alpha_composite(s.stage(im, 1, s.BATTLE, 166, 86), (x, y + 168))
        d.text((x + 2, y + 256), lab, font=f10, fill=s.DIM)
    # ---- 1x line-up
    y = 620
    d.rectangle((16, y, W - 16, y + 130), fill=s.PANEL)
    d.text((26, y + 6), '1x line-up on the battle field: A1 A2 B1 B2, then Hilbert, Hilda, Nate, Rosa, Juno, and the donor classes '
                        '(Backpacker, Ace Trainer snow f/m, Hiker gen 9)', font=f13, fill=s.ACC)
    strip = [fronts[k] for k, _ in FRONTS] + [show.get_native(sp)[0] for sp, _ in REFS] + [kb.native(kb.load(JUNO))[0]] + \
            [show.get_native('sd:' + n)[0] for n in ('backpacker', 'acetrainersnowf', 'acetrainersnow', 'hiker-gen9')]
    bg = Image.new('RGBA', (W - 48, 92), s.BATTLE)
    for i, im in enumerate(strip):
        bg.alpha_composite(im, (8 + i * 84, 8))
    sh.alpha_composite(bg, (32, y + 30))
    # ---- backs
    y = 760
    d.rectangle((16, y, W - 16, y + 690), fill=s.PANEL)
    d.text((26, y + 6), 'EBDX battle backs (file size = 2x art): 5 frames, idle -> wind-up -> throw. Left: ours; the base project\'s '
                        'Red/Leaf frame 0 for comparison. Right: frame 0 in an EBDX-like layout (x=40, bottom of a 512x384 screen) '
                        'with Juno\'s front at file size.', font=f13, fill=s.ACC)
    for j, k in enumerate('AB'):
        frs = backs[k]
        yy = y + 32 + j * 330
        for i, f in enumerate(frs):
            sh.alpha_composite(s.stage(kb.up(f, 1), 2, s.STAGE, 168, 240), (26 + i * 172, yy))
        base = bs.frames('EB:POKEMONTRAINER_%s_back' % ('Red' if k == 'A' else 'Leaf'))[0]
        sh.alpha_composite(s.stage(base, 2, s.STAGE, 168, 240), (26 + 5 * 172 + 12, yy))
        d.text((26, yy + 244), 'PLAYER_%s_back (800x234)%s' % (k, '' if k == 'A' else ''), font=f10, fill=s.TXT)
        d.text((26 + 5 * 172 + 12, yy + 244), 'base %s_back frame 0' % ('Red' if k == 'A' else 'Leaf'), font=f10, fill=s.DIM)
        mock = battle_mock(frs[0], JUNO)
        mz = mock.resize((384, 288), Image.NEAREST) if False else mock
        sh.alpha_composite(mz.crop((0, 0, 512, 320)), (1080 + j * 0, yy - 4)) if False else None
    m1 = battle_mock(backs['A'][0], JUNO); m2 = battle_mock(backs['B'][0], JUNO)
    sh.alpha_composite(m1.crop((0, 64, 512, 384)), (1430, y + 32))
    sh.alpha_composite(m2.crop((0, 64, 512, 384)), (1430, y + 362))
    # ---- overworlds
    y = 1460
    d.rectangle((16, y, W - 16, y + 470), fill=s.PANEL)
    d.text((26, y + 6), 'overworld charsets (down, left, right, up x 4 frames): 4x, then 2x beside Juno and Kestrel (ours) and the '
                        'base project\'s Red and Leaf. Installed to art/out/preview_only/Graphics/Characters/ only.',
           font=f13, fill=s.ACC)
    owa = Image.open(D + '/PLAYER_A_ow_native.png').convert('RGBA'); owb = Image.open(D + '/PLAYER_B_ow_native.png').convert('RGBA')
    sh.alpha_composite(kb.up(kb.on_bg(owa, s.STAGE), 4), (26, y + 32))
    sh.alpha_composite(kb.up(kb.on_bg(owb, s.STAGE), 4), (26 + 272, y + 32))
    others = [owa, owb, kb.native(kb.load(kb.GAME + '/art/out/Graphics/Characters/JUNO.png'))[0],
              kb.native(kb.load(kb.GAME + '/art/out/Graphics/Characters/KESTREL.png'))[0],
              kb.native(kb.load(po.R + 'trainer_POKEMONTRAINER_Red.png'))[0], kb.native(kb.load(po.R + 'trainer_POKEMONTRAINER_Leaf.png'))[0]]
    labs = ['A', 'B', 'Juno', 'Kestrel', 'Red', 'Leaf']
    for i, o in enumerate(others):
        x = 600 + i * 140
        sh.alpha_composite(kb.up(kb.on_bg(o.crop((0, 0, 64, 96)).crop((0, 0, 64, 96)), s.STAGE), 2), (x, y + 32))
        d.text((x, y + 228), labs[i], font=f10, fill=s.DIM)
    # 1x on a grass strip, down row frame 0 of each
    gb = Image.new('RGBA', (600, 60), (104, 152, 88, 255))
    for i, o in enumerate(others):
        for c in range(4):
            gb.alpha_composite(o.crop((c * 16, 0, c * 16 + 16, 24)), (10 + i * 96 + c * 18, 18))
    sh.alpha_composite(kb.up(gb, 2), (600, y + 250))
    d.text((600, y + 376), '2x of 1x art on grass (walking frames, down)', font=f10, fill=s.DIM)
    # ---- donors
    y = 1940
    d.rectangle((16, y, W - 16, Hh - 12), fill=s.PANEL)
    d.text((26, y + 6), 'donors (native, 1x/2x) and what was taken', font=f13, fill=s.ACC)
    x = 26
    for spec, part in DONORS:
        if spec.startswith('file:'):
            dn = kb.native(kb.load(spec[5:]))[0]
            if dn.size[0] > 3 * dn.size[1] // 2 + 10:
                fw = dn.size[0] // 5 if dn.size[0] >= 3 * dn.size[1] else 16
                dn = dn.crop((0, 0, fw, dn.size[1] if fw != 16 else 24))
        else:
            dn = s.donor_img(spec)
        dn = dn.crop(kb.bbox(dn))
        k = 2 if dn.size[1] <= 100 else 1
        z = kb.up(dn, k)
        bgd = Image.new('RGBA', (max(150, z.size[0] + 8), 214), s.STAGE)
        bgd.alpha_composite(z, ((bgd.size[0] - z.size[0]) // 2, 214 - z.size[1] - 4))
        if x + bgd.size[0] > W - 20:
            break
        sh.alpha_composite(bgd, (x, y + 28))
        s.wrap(d, part, (x + 2, y + 246), bgd.size[0] - 4, f10, s.TXT)
        x += bgd.size[0] + 8
    sh.save(kb.GAME + '/art/previews/22_player.png'); print('22_player.png', sh.size)


if __name__ == '__main__':
    main()
