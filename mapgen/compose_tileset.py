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


if __name__ == '__main__':
    main()
