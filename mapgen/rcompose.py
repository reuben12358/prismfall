#!/usr/bin/env python3
"""rcompose.py - the Rejuvenation-family composite sheet "PF Rejuv" and the tilesets that use it (MAPGEN 2h).

One tall sheet = whole sheets from the downloaded games appended in a FIXED order (new parts only ever go at the end,
so ids never move).  Several tileset ids share the sheet, each with its own 7 autotiles, exactly as Rejuvenation
itself does (its tilesets 62/85/21 share `Goldenleaf Forrest`).
  composite id = part offset + (source id - 384)
Passages / priorities / terrain tags come from each part's source Tilesets.rxdata (safe parser). Terrain tags 17+ use
these games' numbering (Scripts/Field.rb) and are remapped with TAG_REMAP_GAMES (GAMES_READY.md).
Autotiles are copied with a prefix ("RJ ", "RB ") so they can never overwrite a project's stock `Sea.png` etc.

Virtual autotile ids: layouts and learned tables refer to an autotile by its source name, never by slot. A virtual id
is VBASE + 48 * index-in-AUTOS + shape; `resolve(layers, tileset_id)` turns them into that tileset's slot ids.

    python3 -I rcompose.py          # writes the sheet, autotile copies, registers ids 50-53, data/rj_compose.json"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import rmarshal as M
import rref as RR
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
REG = os.path.join(OUT, 'tilesets_prismfall.json')
SHEET = 'PF Rejuv'
TAG_REMAP_GAMES = {17: 0, 18: 16, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 3, 25: 3, 26: 0, 27: 0, 28: 0, 29: 5}

# (key, game, source tileset id for passages, sheet file).  APPEND ONLY.
PARTS = [('gl', 'rejuvenation', 62, 'Goldenleaf Forrest'),
         ('sh', 'rejuvenation', 126, 'Sheridan_2'),
         ('ak', 'rejuvenation', 211, 'Route 4'),
         ('kf', 'rejuvenation', 93, 'Kristiline Town (Frozen)'),
         ('rb4', 'reborn', 43, 'Route4'),
         ('ap', 'rejuvenation', 2, 'Aevium Past'),
         ('pf', None, None, None)]          # Prismfall custom pieces (rj_custom.png, built by rcustom.py)
CUSTOM_ROWS = 64

# every autotile any PF Rejuv tileset may use: (game, source tileset whose passages it takes, source name)
AUTOS = [('rejuvenation', 126, 'Sea(Grass)'), ('rejuvenation', 126, 'DirtDark'), ('rejuvenation', 127, 'Dirt'),
         ('rejuvenation', 62, 'Gravel(G)'), ('rejuvenation', 62, 'Sea'), ('rejuvenation', 126, 'Waterfall crest'),
         ('rejuvenation', 126, 'Waterfall'), ('rejuvenation', 126, 'Waterfall bottom'), ('rejuvenation', 211, 'Ocean'),
         ('rejuvenation', 211, 'Sand shore_2'), ('rejuvenation', 211, 'Sea deep'), ('rejuvenation', 211, 'Dirt Route 4'),
         ('rejuvenation', 211, 'stillwaterr4'), ('rejuvenation', 93, 'KristilineWatersFrozen'),
         ('rejuvenation', 93, 'KristilineDirt'), ('rejuvenation', 93, 'Ocean(Terajuma)_2'),
         ('rejuvenation', 93, 'Sand shore(Terajuma)'), ('rejuvenation', 93, 'Waterfall crest (T)'),
         ('rejuvenation', 93, 'Waterfall (1)'), ('rejuvenation', 93, 'Waterfall bottom (T)'),
         ('reborn', 43, 'Still water grey'), ('reborn', 43, 'Still water snow'), ('rejuvenation', 62, 'Still water'),
         ('rejuvenation', 2, 'White path2'), ('rejuvenation', 7, 'Sand shore'),
         ('rejuvenation', 2, 'Hoenn Sea'), ('rejuvenation', 7, 'Dirt Route 5'), ('rejuvenation', 2, 'Still water - Copy'),
         ('pf', 62, 'Gravel Spring')]
# derived autotiles: name -> (source game, source name, colour map).  Gravel(G)'s autumn-yellow verge becomes Sheridan's
# spring grass (the same two colours DirtDark's verge uses), so the Goldenleaf street gravel sits on green ground.
DERIVED = {'Gravel Spring': ('rejuvenation', 'Gravel(G)', {(213, 184, 68): (168, 216, 160), (173, 133, 72): (112, 200, 160)})}
VBASE = 100000
PREFIX = {'rejuvenation': 'RJ ', 'reborn': 'RB ', 'pf': 'PF '}
# tileset id -> (name, autotile keys (game, name), biome note).  The sheet is shared.
TILESETS = {
    50: ('PF Rejuv Village', [('rejuvenation', 'Sea(Grass)'), ('rejuvenation', 'DirtDark'), ('rejuvenation', 'Waterfall crest'),
                              ('rejuvenation', 'Waterfall'), ('rejuvenation', 'Waterfall bottom'), ('pf', 'Gravel Spring'),
                              ('rejuvenation', 'Dirt')]),
    51: ('PF Rejuv Coast', [('rejuvenation', 'Sea(Grass)'), ('rejuvenation', 'DirtDark'), ('rejuvenation', 'Ocean'),
                            ('rejuvenation', 'Sand shore_2'), ('rejuvenation', 'Sea deep'), ('pf', 'Gravel Spring'),
                            ('rejuvenation', 'Dirt')]),
    52: ('PF Rejuv Snow', [('rejuvenation', 'KristilineWatersFrozen'), ('rejuvenation', 'KristilineDirt'),
                           ('rejuvenation', 'Ocean(Terajuma)_2'), ('rejuvenation', 'Sand shore(Terajuma)'),
                           ('rejuvenation', 'Waterfall crest (T)'), ('rejuvenation', 'Waterfall (1)'), ('reborn', 'Still water snow')]),
    53: ('PF Rejuv Wild', [('rejuvenation', 'Sea(Grass)'), ('rejuvenation', 'DirtDark'), ('rejuvenation', 'Dirt'),
                           ('rejuvenation', 'Gravel(G)'), ('rejuvenation', 'Still water'), ('rejuvenation', 'Waterfall'),
                           ('rejuvenation', 'Waterfall bottom')]),
}
_CFG = None


def cfg():
    global _CFG
    if _CFG is None:
        _CFG = json.load(open(os.path.join(HERE, 'data', 'rj_compose.json')))
    return _CFG


def offset(key):
    return cfg()['parts'][key]['offset']


def vauto(game, name, shape=0):
    i = next(k for k, a in enumerate(AUTOS) if a[0] == game and a[2] == name)
    return VBASE + 48 * i + shape


def vauto_name(v):
    a = AUTOS[(v - VBASE) // 48]; return a[0], a[2]


def to_composite(L, game, src_tileset, part):
    """A reference map's layers -> composite ids (sheet tiles) and virtual autotile ids; unknown autotiles -> -1."""
    ts = RR.tileset(game, src_tileset); off = offset(part)
    out = np.zeros_like(L)
    sheet = L >= 384
    out[sheet] = L[sheet] - 384 + off
    au = (L >= 48) & (L < 384)
    for v in np.unique(L[au]):
        nm = ts['autotile_names'][v // 48 - 1]
        try: out[L == v] = vauto(game, nm, v % 48)
        except StopIteration: out[L == v] = -1
    return out


def resolve(L, tid):
    """Virtual autotile ids -> slot ids of tileset `tid` (raises on an autotile the tileset lacks)."""
    keys = TILESETS[tid][1]
    out = L.copy()
    v = L >= VBASE
    for val in np.unique(L[v]):
        g, n = vauto_name(int(val))
        if (g, n) not in keys:
            raise ValueError('autotile %s/%s is not in tileset %d %s' % (g, n, tid, TILESETS[tid][0]))
        out[L == val] = (keys.index((g, n)) + 1) * 48 + (int(val) - VBASE) % 48
    out[out < 0] = 0
    return out


def main():
    ims = []; pas = [0] * 384; pri = [0] * 384; tag = [0] * 384; parts = {}
    src_ts = {}
    for key, game, tid, fname in PARTS:
        if key == 'pf':
            p = os.path.join(HERE, 'data', 'rj_custom.png')
            im = Image.open(p).convert('RGBA') if os.path.exists(p) else Image.new('RGBA', (256, CUSTOM_ROWS * 32))
            im = im.crop((0, 0, 256, CUSTOM_ROWS * 32)); n = CUSTOM_ROWS * 8
            cp = os.path.join(HERE, 'data', 'rj_custom.json')
            cprops = json.load(open(cp)) if os.path.exists(cp) else {}
            parts[key] = {'offset': len(pas), 'tiles': n}
            p_ = [15] * n; q_ = [0] * n; t_ = [0] * n
            for i, (a, b, c) in cprops.get('props', {}).items():
                p_[int(i)], q_[int(i)], t_[int(i)] = a, b, c
            pas += p_; pri += q_; tag += t_; ims.append(im); continue
        im = Image.open(os.path.join(RR.GAMES[game], 'Graphics', 'Tilesets', fname + '.png')).convert('RGBA')
        im = im.crop((0, 0, 256, im.height // 32 * 32)); n = im.height // 32 * 8
        t = RR.tileset(game, tid)
        parts[key] = {'offset': len(pas), 'tiles': n, 'game': game, 'src_tileset': tid, 'sheet': fname}
        p = t['passages'][384:384 + n]; q = t['priorities'][384:384 + n]
        g = [x if x <= 16 else TAG_REMAP_GAMES.get(x, 0) for x in t['terrain_tags'][384:384 + n]]
        pas += p + [0] * (n - len(p)); pri += q + [0] * (n - len(q)); tag += g + [0] * (n - len(g))
        ims.append(im)
    H = sum(i.height for i in ims)
    sheet = Image.new('RGBA', (256, H)); y = 0
    for i in ims: sheet.paste(i, (0, y)); y += i.height
    os.makedirs(os.path.join(OUT, 'Graphics', 'Tilesets'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'Graphics', 'Autotiles'), exist_ok=True)
    sheet.save(os.path.join(OUT, 'Graphics', 'Tilesets', SHEET + '.png'))
    autos = []
    for game, tid, name in AUTOS:
        dst_name = PREFIX[game] + name
        if game == 'pf':
            sg, sn, cmap = DERIVED[name]
            im = Image.open(os.path.join(RR.GAMES[sg], 'Graphics', 'Autotiles', sn + '.png')).convert('RGBA'); px = im.load()
            for yy in range(im.height):
                for xx in range(im.width):
                    r, g_, b, al = px[xx, yy]
                    if al and (r, g_, b) in cmap: px[xx, yy] = cmap[(r, g_, b)] + (al,)
            im.save(os.path.join(OUT, 'Graphics', 'Autotiles', dst_name + '.png'))
            t = RR.tileset(sg, tid); s = t['autotile_names'].index(sn) + 1
        else:
            src = os.path.join(RR.GAMES[game], 'Graphics', 'Autotiles', name + '.png')
            Image.open(src).save(os.path.join(OUT, 'Graphics', 'Autotiles', dst_name + '.png'))
            t = RR.tileset(game, tid); s = t['autotile_names'].index(name) + 1
        autos.append(dict(game=game, name=name, file=dst_name, passages=t['passages'][48 * s:48 * s + 48],
                          priorities=t['priorities'][48 * s:48 * s + 48],
                          tags=[x if x <= 16 else TAG_REMAP_GAMES.get(x, 0) for x in t['terrain_tags'][48 * s:48 * s + 48]]))
    json.dump({'sheet': SHEET, 'parts': parts, 'n_tiles': len(pas)}, open(os.path.join(HERE, 'data', 'rj_compose.json'), 'w'), indent=1)
    reg = json.load(open(REG)) if os.path.exists(REG) else []
    for tid, (name, keys) in TILESETS.items():
        p, q, g = list(pas), list(pri), list(tag)
        names = []
        for s, (game, an) in enumerate(keys, 1):
            a = next(a for a in autos if a['game'] == game and a['name'] == an)
            names.append(a['file'])
            p[48 * s:48 * s + 48] = a['passages']; q[48 * s:48 * s + 48] = a['priorities']; g[48 * s:48 * s + 48] = a['tags']
        names += [''] * (7 - len(names))
        e = dict(id=tid, name=name, tileset_name=SHEET, autotile_names=names, panorama='', fog='', battleback='',
                 n_tiles=len(p), passages=p, priorities=q, terrain_tags=g)
        reg = [t for t in reg if t['id'] != tid] + [e]
        print('registered %d %s: %d tiles, autotiles %s' % (tid, name, len(p) - 384, names))
    json.dump(sorted(reg, key=lambda t: t['id']), open(REG, 'w'))
    print('sheet %s: %d rows; parts %s' % (SHEET, H // 32, {k: v['offset'] for k, v in parts.items()}))


if __name__ == '__main__':
    main()
