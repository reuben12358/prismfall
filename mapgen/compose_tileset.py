#!/usr/bin/env python3
"""compose_tileset.py - build the composite tileset 33 "Prismfall City": Tectonic's Outside sheet (ids unchanged, so
the `tectonic` painters, learned tables and stamps keep working) with whole Rejuvenation sheets appended below it.
RMXP maps use one tileset each, so mixing Sheridan's timber houses with the Tectonic castle kit needs one sheet.
Appended tile id = OFFSET[sheet] + (source id - 384). Passages and priorities come from each source Tilesets.rxdata
(safe parser); appended terrain tags are zeroed (Rejuvenation's tag numbers differ from v21.1). Autotiles = Tectonic's.
Writes maps_out/Graphics/Tilesets/Prismfall City.png, registers id 33, and writes data/compose_offsets.json."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import rmarshal as M
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
REG = os.path.join(OUT, 'tilesets_prismfall.json')
WLL = '/home/claude/ref/art/wll/Changed Files'
PARTS = [('sheridan', 37, 'Sheridan_2'), ('gearen', 1, 'GearenCity Real')]
Image.MAX_IMAGE_PIXELS = None


def main():
    reg = json.load(open(REG))
    base = next(t for t in reg if t['id'] == 30)
    ims = [Image.open(os.path.join(OUT, 'Graphics', 'Tilesets', base['tileset_name'] + '.png')).convert('RGBA')]
    pas, pri, tag = list(base['passages']), list(base['priorities']), list(base['terrain_tags'])
    n0 = 384 + ims[0].height // 32 * 8
    pas, pri, tag = (v[:n0] + [0] * (n0 - len(v)) for v in (pas, pri, tag))
    wt = M.load_file(os.path.join(WLL, 'Data', 'Tilesets.rxdata'))
    offs = {}
    for key, tid, fname in PARTS:
        im = Image.open(os.path.join(WLL, 'Graphics', 'Tilesets', fname + '.png')).convert('RGBA')
        im = im.crop((0, 0, 256, im.height // 32 * 32))
        n = im.height // 32 * 8
        offs[key] = {'offset': len(pas), 'tiles': n, 'src_tilesets': [tid]}
        t = wt[tid]
        p = [int(x) for x in t.passages.data.reshape(-1)][384:384 + n]; q = [int(x) for x in t.priorities.data.reshape(-1)][384:384 + n]
        pas += p + [0] * (n - len(p)); pri += q + [0] * (n - len(q)); tag += [0] * n
        ims.append(im)
    # custom Prismfall pieces (ref/art/custom, Art Director prototypes): realm banners (1x2 each, 8 across) and a throne (2x3)
    cu = Image.new('RGBA', (256, 160), (0, 0, 0, 0))
    cu.paste(Image.open('/home/claude/ref/art/custom/banners_1x2_x8.png').convert('RGBA'), (0, 0))
    cu.paste(Image.open('/home/claude/ref/art/custom/throne_2x3_crownhaven.png').convert('RGBA'), (0, 64))
    offs['custom'] = {'offset': len(pas), 'tiles': 40, 'src_tilesets': []}
    pas += [15] * 40; pri += [0] * 40; tag += [0] * 40; ims.append(cu)
    # recoloured Sheridan sheets (roof and timber browns -> slate / moss) so the eight timber houses do not all match
    import colorsys
    src = Image.open(os.path.join(WLL, 'Graphics', 'Tilesets', 'Sheridan_2.png')).convert('RGBA')
    src = src.crop((0, 0, 256, src.height // 32 * 32)); st = wt[37]; n = src.height // 32 * 8
    for key, (hue, sm, vm) in (('sheridan_slate', (0.60, 0.45, 1.0)), ('sheridan_moss', (0.36, 0.75, 0.9))):
        im = src.copy(); px = im.load(); cache = {}
        for y in range(im.height):
            for x in range(256):
                r, g, b, a = px[x, y]
                if a == 0: continue
                k = (r, g, b)
                if k not in cache:
                    h, s_, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
                    if 0.0 <= h <= 0.11 and s_ > 0.3 and v < 0.8:
                        cache[k] = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, s_ * sm, v * vm))
                    else: cache[k] = k
                px[x, y] = cache[k] + (a,)
        offs[key] = {'offset': len(pas), 'tiles': n, 'src_tilesets': [37]}
        p = [int(v) for v in st.passages.data.reshape(-1)][384:384 + n]; q = [int(v) for v in st.priorities.data.reshape(-1)][384:384 + n]
        pas += p + [0] * (n - len(p)); pri += q + [0] * (n - len(q)); tag += [0] * n; ims.append(im)
    # second custom block (make_custom.py): giant-tree boles and crowns, silk awnings, laundry lines, light pools ...
    c2 = os.path.join(HERE, 'custom', 'prismfall_custom2.png')
    if os.path.exists(c2):
        im = Image.open(c2).convert('RGBA'); n = im.height // 32 * 8
        meta = json.load(open(c2[:-4] + '.json'))
        offs['custom2'] = {'offset': len(pas), 'tiles': n, 'src_tilesets': []}
        pas += [int(v) for v in meta['passages']]; pri += [int(v) for v in meta['priorities']]; tag += [0] * n; ims.append(im)
    sheet = Image.new('RGBA', (256, sum(i.height for i in ims)), (0, 0, 0, 0)); y = 0
    for i in ims:
        sheet.paste(i, (0, y)); y += i.height
    sheet.save(os.path.join(OUT, 'Graphics', 'Tilesets', 'Prismfall City.png'))
    e = dict(base); e.update(id=33, name='Prismfall City', tileset_name='Prismfall City', n_tiles=len(pas), passages=pas,
                             priorities=pri, terrain_tags=tag)
    reg = [t for t in reg if t['id'] != 33] + [e]
    json.dump(sorted(reg, key=lambda t: t['id']), open(REG, 'w'))
    json.dump(offs, open(os.path.join(HERE, 'data', 'compose_offsets.json'), 'w'))
    print('tileset 33: %d tiles, sheet %dx%d, offsets %s' % (len(pas) - 384, sheet.width, sheet.height, offs))


def interior():
    """Tileset 34 "Prismfall Interior": Tectonic's Inside sheet (ids unchanged, its autotiles) + Rejuvenation interior sheets."""
    import shutil
    TG = '/home/claude/ref/art/tectonic'
    tt = M.load_file(os.path.join(TG, 'Data', 'Tilesets.rxdata'))[25]
    wt = M.load_file(os.path.join(WLL, 'Data', 'Tilesets.rxdata'))
    im0 = Image.open(os.path.join(TG, 'Graphics', 'Tilesets', tt.tileset_name + '.png')).convert('RGBA')
    im0 = im0.crop((0, 0, 256, im0.height // 32 * 32)); n0 = 384 + im0.height // 32 * 8
    fix = lambda v: ([int(x) for x in v.data.reshape(-1)] + [0] * n0)[:n0]
    pas, pri = fix(tt.passages), fix(tt.priorities); tag = [x if x <= 16 else 0 for x in fix(tt.terrain_tags)]
    ims = [im0]; offs = json.load(open(os.path.join(HERE, 'data', 'compose_offsets.json')))
    for key, tid, fname in (('in_sheridan', 38, 'SheridanInside'), ('in_help', 29, 'Help Centers'), ('in_hotel', 3, 'Chrisola Hotel'),
                            ('in_theatre', 36, 'RoseTheatre')):
        im = Image.open(os.path.join(WLL, 'Graphics', 'Tilesets', fname + '.png')).convert('RGBA')
        im = im.crop((0, 0, 256, im.height // 32 * 32)); n = im.height // 32 * 8; t = wt[tid]
        offs[key] = {'offset': len(pas), 'tiles': n, 'src_tilesets': [tid]}
        p = [int(x) for x in t.passages.data.reshape(-1)][384:384 + n]; q = [int(x) for x in t.priorities.data.reshape(-1)][384:384 + n]
        pas += p + [0] * (n - len(p)); pri += q + [0] * (n - len(q)); tag += [0] * n; ims.append(im)
    sheet = Image.new('RGBA', (256, sum(i.height for i in ims)), (0, 0, 0, 0)); y = 0
    for i in ims:
        sheet.paste(i, (0, y)); y += i.height
    sheet.save(os.path.join(OUT, 'Graphics', 'Tilesets', 'Prismfall Interior.png'))
    for nme in tt.autotile_names:
        if nme: shutil.copyfile(os.path.join(TG, 'Graphics', 'Autotiles', nme + '.png'), os.path.join(OUT, 'Graphics', 'Autotiles', nme + '.png'))
    e = dict(id=34, name='Prismfall Interior', tileset_name='Prismfall Interior', autotile_names=list(tt.autotile_names), panorama='',
             fog='', battleback='', n_tiles=len(pas), passages=pas, priorities=pri, terrain_tags=tag)
    reg = [t for t in json.load(open(REG)) if t['id'] != 34] + [e]
    json.dump(sorted(reg, key=lambda t: t['id']), open(REG, 'w'))
    json.dump(offs, open(os.path.join(HERE, 'data', 'compose_offsets.json'), 'w'))
    print('tileset 34: %d tiles' % (len(pas) - 384), {k: v['offset'] for k, v in offs.items() if k.startswith('in_')}, tt.autotile_names)


if __name__ == '__main__':
    main(); interior()
