"""Build the three study moodboards (not shipped in the game).
python3 -I art/research/scripts/moodboards.py
Tiles: (key, crop, caption-title, caption-lesson). key = 'R:<art_refs path>' | 'G:<ref/games path>' | 'A:<abs path>' | 'VS:<trainer png>'."""
import sys, os
sys.path.insert(0, '/home/claude/fangame/tools/kitbash')
import kb
from PIL import Image, ImageDraw, ImageFont
R = '/home/claude/ref/art_refs/'; G = '/home/claude/ref/games/'; OUT = '/home/claude/fangame/art/research/'
B2 = '/home/claude/ref/art/sprites_gen5_vs_tech/extracted/Gen 5 VS Sprites/'
FONT = kb.font(13); FONT_S = kb.font(11); FONT_H = kb.font(20)


def load_key(key):
    kind, path = key.split(':', 1)
    if kind == 'VS':
        t = kb.native(kb.load(path))[0]; b = path.replace('vsTrainer', 'vsBar')
        bg = kb.load(b) if os.path.exists(b) else Image.new('RGBA', t.size, (90, 90, 110, 255))
        if bg.size != t.size: bg = bg.resize(t.size, Image.NEAREST)
        return Image.alpha_composite(bg, t), True
    p = {'R': R, 'G': G, 'A': ''}[kind] + path
    im = Image.open(p).convert('RGBA')
    pixel = kind in ('G', 'A') or 'pixel' in path
    return im, pixel


def fit(im, box_w, box_h, pixel):
    if pixel:
        # undo integer upscales first, then nearest-neighbour to the largest integer that fits
        try:
            n = kb.native(im)[0]
            if n.size[0] * 2 <= im.size[0] or n.size == im.size: im = n
        except Exception:
            pass
        k = max(1, min(box_w // im.width, box_h // im.height))
        if k >= 1 and im.width * k <= box_w and im.height * k <= box_h:
            return im.resize((im.width * k, im.height * k), Image.NEAREST)
    s = min(box_w / im.width, box_h / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def board(name, title, sub, tiles, cols, tw, th):
    cap = 46; pad = 10
    rows = (len(tiles) + cols - 1) // cols
    W = cols * (tw + pad) + pad; H = 70 + rows * (th + cap + pad) + pad
    S = Image.new('RGBA', (W, H), (34, 34, 40, 255)); d = ImageDraw.Draw(S)
    d.text((pad, 10), title, font=FONT_H, fill=(240, 230, 200, 255))
    d.text((pad, 40), sub, font=FONT_S, fill=(200, 200, 210, 255))
    for i, (key, crop, t1, t2) in enumerate(tiles):
        im, pixel = load_key(key)
        if crop: im = im.crop(crop)
        x = pad + (i % cols) * (tw + pad); y = 70 + (i // cols) * (th + cap + pad)
        cell = Image.new('RGBA', (tw, th), (150, 150, 162, 255))
        f = fit(im, tw, th, pixel)
        cell.alpha_composite(f, ((tw - f.width) // 2, (th - f.height) // 2))
        S.alpha_composite(cell, (x, y))
        d.text((x, y + th + 3), t1, font=FONT, fill=(250, 220, 150, 255))
        d.text((x, y + th + 21), t2, font=FONT_S, fill=(215, 215, 222, 255))
    S.convert('RGB').save(OUT + name, optimize=True)
    print(name, S.size, len(tiles))


AC = (208, 0, 768, 549)
PORTRAITS = [
    ('A:/home/claude/fangame/art/out/Graphics/Portraits/JUNO_happy.png', None, 'OURS: Juno pass 3 (accepted anchor)', '48px art x2, black outline, 2-tone cel, big eyes'),
    ('G:desolation/Graphics/Faces/13.png', None, 'Desolation Faces/13', 'eye line ~row 20/48; head overfills top'),
    ('G:desolation/Graphics/Faces/08a.png', None, 'Desolation Faces/08a', '3/4 view, 2px lash + outer flick'),
    ('G:desolation/Graphics/Faces/22.png', None, 'Desolation Faces/22', 'silver hair = blue-grey ramp, not grey'),
    ('G:desolation/Graphics/Faces/18.png', None, 'Desolation Faces/18', 'hat brim may break the frame'),
    ('G:desolation/Graphics/Faces/10a.png', None, 'Desolation Faces/10a', 'adult male: brow mass, jaw plane, grin'),
    ('VS:' + B2 + 'vsTrainer_POKEMONTRAINER_Bianca.png', (37, 0, 85, 48), 'B2W2 VS Bianca (48px crop)', 'official look: flat, bright, 1 highlight'),
    ('VS:' + B2 + 'vsTrainer_LEADER_Skyla.png', (40, 0, 88, 48), 'B2W2 VS Skyla (48px crop)', 'open grin: teeth row + tongue tone'),
    ('R:honnojis/momo_pixel.png', None, 'honnojis: momo pixel (100px)', 'coloured inner lines, 21 colours'),
    ('R:honnojis/okarun_pixel.png', None, 'honnojis: okarun pixel (100px)', 'hue-shifted shadows, mint accent'),
    ('R:vgen_angeceleste/04.png', AC, 'angeceleste (VGen) pixel icon', 'freckles 1px, heavy lash wing'),
    ('R:vgen_angeceleste/06.png', AC, 'angeceleste (VGen) pixel icon', 'blush hatch, teal accent vs purple'),
    ('R:vgen_angeceleste/03.png', AC, 'angeceleste (VGen) pixel icon', 'white sticker rim on flat colour bg'),
    ('R:vgen_fiorne/01.png', None, 'Fiorne (VGen) dialogue portrait', 'framed face beside the text box'),
    ('R:vgen_mossgrover/03.png', None, 'Mossgrover (VGen) 64x64 talker', 'tiny portrait: big eyes, 2 frames'),
    ('R:vgen_noodlesxl/14.png', None, 'NoodlesXL (VGen) FoM portrait', 'clean bright bust, sky plate bg'),
    ('R:vgen_noodlesxl/09.png', None, 'NoodlesXL (VGen) cute portrait', 'symmetry = calm; colour-block hair'),
    ('R:vgen_honnojis/chibi_14.png', None, 'honnojis (VGen) chibi', 'flat disc behind head, navy outline'),
    ('R:honnojis/pom_ref_sheet_v3.png', (860, 40, 1200, 1080), 'honnojis: Pom expressions', 'one face, 5 attitudes; props in frame'),
    ('R:honnojis/damian_ref_sheet_v3.png', (620, 0, 1200, 640), 'honnojis: Damian expressions', 'expression = brows+mouth+sweat marks'),
]
CHARACTERS = [
    ('R:honnojis/juno_ref_portfolio.png', (0, 0, 470, 560), 'honnojis: silhouette + value roughs', '24 black thumbnails -> 4 value roughs'),
    ('R:honnojis/juno_ref_portfolio.png', None, 'honnojis: ref sheet (her OC "Juno")', 'turnaround + hero pose; red accent'),
    ('R:honnojis/damian_ref_sheet_v3.png', None, 'honnojis: Damian ref sheet', 'palette strip; motif repeats (rose)'),
    ('R:honnojis/pom_ref_sheet_v3.png', None, 'honnojis: Pom ref sheet', '3 colours + 1 accent; asym. hair tuft'),
    ('R:honnojis/key_art_2021.png', None, 'honnojis: key art 2021', 'cast read by colour block + shape'),
    ('R:honnojis/tarot_01_magician.png', None, 'honnojis: The Magician', 'bright, big-eyed, warm/cool split'),
    ('R:honnojis/rejuv_illust.png', None, 'honnojis: Rejuvenation illust', 'hard cel shadow, warm key/teal fill'),
    ('R:honnojis/v14_cover_art.png', None, 'honnojis: Rejuv V14 cover', 'VS energy: diagonal split, glint'),
    ('R:honnojis/full_illust_penny.png', None, 'honnojis: Penny illust', 'shape language: round = warm'),
    ('R:honnojis/rejuv_illust_bsky.png', None, 'honnojis: Rejuvenation illust 2', 'one light source, rim light'),
    ('R:honnojis/aelita_wallpaper.png', None, 'honnojis: Aelita (Rejuvenation)', 'character + partner Pokemon staging'),
    ('R:vgen_ngreentail/02.png', None, 'Nifast Greentail: Pokemon (old)', 'Sugimori-era colour, layered frills'),
    ('R:vgen_ngreentail/03.png', None, 'Nifast Greentail: Pokemon (old)', 'type motif worked into costume'),
    ('R:vgen_ngreentail/04.png', None, 'Nifast Greentail: Pokemon (old)', 'Pokemon motif as hair/clothes'),
    ('R:vgen_princeloppy/04.png', None, 'Princeloppy: Pokemon style', 'thin line, 2 tones, soft round shapes'),
    ('R:vgen_princeloppy/07.png', None, 'Princeloppy: Pokemon style', 'costume layering, accent at neck'),
    ('R:vgen_silversrini/01.png', None, 'SilverSrini: trainer + partner', 'trainer and Pokemon share a palette'),
    ('R:vgen_angeceleste/01.png', None, 'angeceleste: trainer sprite art', 'partner colours echo the outfit'),
]
PIXEL = [
    ('VS:' + B2 + 'vsTrainer_POKEMONTRAINER_Bianca.png', None, 'B2W2 VS Bianca (official)', 'bar = signature hue, bust breaks top'),
    ('VS:' + B2 + 'vsTrainer_LEADER_Skyla.png', None, 'B2W2 VS Skyla (official)', 'gesture hand in the foreground'),
    ('VS:' + B2 + 'vsTrainer_LEADER_Roxie.png', None, 'B2W2 VS Roxie (official)', 'prop diagonal crosses the bar'),
    ('VS:' + B2 + 'vsTrainer_LEADER_Lenora.png', None, 'B2W2 VS Lenora (official)', 'pointing finger = personality'),
    ('VS:' + G + 'rejuvenation/Graphics/Transitions/vsTrainer192.png', None, 'Rejuvenation VS 192', 'smug squint, dark-red bar'),
    ('VS:' + G + 'rejuvenation/Graphics/Transitions/vsTrainer79.png', None, 'Rejuvenation VS 79', 'big laugh + sweeping arm'),
    ('VS:' + G + 'desolation/Graphics/Transitions/vsTrainer124.png', None, 'Desolation VS 124', 'reach toward camera'),
    ('VS:' + G + 'reborn/Graphics/Transitions/vsTrainer227.png', None, 'Reborn VS 227', 'card prop = character hook'),
    ('R:vgen_noodlesxl/10.png', (208, 0, 768, 549), 'NoodlesXL: trainer + VS (VGen)', 'front, VS bust, partner, one palette'),
    ('R:vgen_noodlesxl/12.png', (0, 120, 976, 432), 'NoodlesXL: VS banner (VGen)', 'B2W2 bar language, white VS'),
    ('R:vgen_noodlesxl/11.png', (208, 0, 768, 549), 'NoodlesXL: B2W2-style front', 'pastel, 1px dark outline, twirl pose'),
    ('R:vgen_noodlesxl/13.png', (316, 110, 713, 439), 'NoodlesXL: front + battler', 'hat + cape silhouette at 80px'),
    ('G:rejuvenation/Graphics/Characters/trainer021.png', None, 'Rejuvenation front 021', 'round body = warm; prop cane'),
    ('G:rejuvenation/Graphics/Characters/trainer240.png', None, 'Rejuvenation front 240', 'lunge pose, cape diagonal'),
    ('G:reborn/Graphics/Characters/trainer193.png', None, 'Reborn front 193', 'clean 80px: 3 tones per material'),
    ('A:/home/claude/ref/art/sprites_kyledove_swsh/sprites/MUSICIAN.png', None, 'kyledove: Gen5-style front', 'performer pose reads at 1x'),
    ('A:/home/claude/ref/art/sprites_kyledove_swsh/sprites/DANCER.png', None, 'kyledove: Gen5-style front', 'mid-motion, weight on one leg'),
    ('A:/home/claude/fangame/art/out/Graphics/Characters/JUNO.png', (0, 0, 128, 48), 'OURS: Juno overworld (installed)', '16x24 art x2; hair = silhouette'),
    ('G:rejuvenation/Graphics/Characters/Aelita.png', (0, 0, 192, 48), 'Rejuvenation overworld', 'head ~half the height, 1x2 eyes'),
    ('R:honnojis/momo_pixel.png', None, 'honnojis: momo pixel', 'no dithering; clusters >= 2px'),
    ('R:vgen_princeloppy/03.png', None, 'Princeloppy: pixel sprites', 'tiny figures: 1 accent colour each'),
    ('A:/home/claude/ref/art/sprites_gen4_ow_vanillasunshine/extracted/trchar092.png', None, 'VanillaSunshine: Gen 4 overworlds', 'walk cycle: 4 frames x 4 facings'),
]

if __name__ == '__main__':
    board('moodboard_portraits.png', 'Moodboard: 96x96 dialogue portraits (study only, not shipped)',
          'Desolation/Rejuvenation Faces, official B2W2 VS crops, honnojis pixel pieces, VGen pixel-portrait artists. See SOURCES.md.', PORTRAITS, 5, 300, 250)
    board('moodboard_characters.png', 'Moodboard: character design, costume, silhouette (study only)',
          'honnojis (official Rejuvenation artist) ref sheets + illustrations; VGen Pokemon-style artists. Learn principles; never copy a piece.', CHARACTERS, 6, 280, 300)
    board('moodboard_pixel.png', 'Moodboard: pixel sprites - VS bars, battle fronts, overworlds (study only)',
          'Official B2W2 VS, Rejuvenation/Desolation/Reborn in-game art, NoodlesXL/kyledove/Princeloppy/Mossgrover. Pixel art shown at integer zoom.', PIXEL, 6, 300, 200)
