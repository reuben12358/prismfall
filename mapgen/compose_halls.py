#!/usr/bin/env python3
"""compose_halls.py - tileset 54 "PF Rejuv Halls": the puzzle interiors (Gym 1 Pell Playhouse, Gym 2 Loomhouse and its Canopy).

A compact sheet in the PF Rejuv family (owner: puzzle engineer; nothing here touches tilesets 50-53):
  mi  Rejuvenation `Multi-Interiors` (timber halls: Sensei's House, Goldenleaf interiors) - only the sheet rows that
      the reference maps MI_MAPS use, kept as whole rows in sheet order so multi-tile objects stay intact
  mg  Rejuvenation `Multi-Gym Interior` (Goldenleaf Theatre, Backstage) - rows used by MG_MAPS
  pf  Prismfall's own silk props (loom, dye vats, webs, strands, lanterns) copied from the PF Rejuv sheet
  cu  puzzle pieces made here: tinted copies of the sheet's own timber and curtain tiles (planks, scenery drops,
      hanging flats) and small drawn markers (threads, heddles, marks, treadles)
Only tiles are taken; every layout is ours. The games are read with the safe parser (rref), nothing is executed.
Writes maps_out/Graphics/Tilesets/PF Rejuv Halls.png, registers id 54, writes data/halls.json:
  {"mi": {"<src id>": id}, "mg": {...}, "pf": {"<PF Rejuv id>": id}, "cu": {"name": id}}

    python3 -I compose_halls.py"""
import os, sys, json, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import rref as RR
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
REG = os.path.join(OUT, 'tilesets_prismfall.json')
TID, NAME = 54, 'PF Rejuv Halls'
MI = ('rejuvenation', 17, 'Multi-Interiors', (7, 17, 220))
MG = ('rejuvenation', 120, 'Multi-Gym Interior', (400, 401))
NM = ('rejuvenation', 123, 'Nightmare City', (151,))      # Nightbox Theater: box seats, chandeliers, velvet seats, the mask banner
CH = ('rejuvenation', 72, 'Chrisola Hotel', [45, 46, 47, 48, 135, 136, 137])   # sheet rows: the grand pianos (side view, open from above)
SOLID_PF = (17876, 17877)      # the loom's upper row: looms are walls between the Weaving Hall's walkways
SOLID_MG = (4691, 4692, 4697,  # theatre seats and the house curtain's fringe: solid (the aisles are the way through)
            4704, 4705, 4706, 4712, 4713, 4714, 4720, 4721, 4722, 4634, 4635, 4636, 4642, 4643, 4644, 4650, 4651, 4652,
            5184, 5185, 5186, 5192, 5193, 5194, 5200, 5201, 5202)   # wall posters: never a way onto the wall
BARK = [18036, 18037, 18038, 18039, 18044, 18045, 18046, 18047, 18052, 18053, 18054, 18055]   # the elder tree's mossy bark
PF_STAMPS = ['pf_p_lantern', 'pf_p_silk', 'pf_p_silk1', 'pf_p_strand_w', 'pf_p_strand_p', 'pf_p_web', 'pf_p_web1', 'pf_p_loom',
             'pf_p_vat_b', 'pf_p_vat_r', 'pf_p_vat_y', 'pf_p_laundry', 'pf_p_awning', 'pf_lantern',
             'hb_dyeline', 'hb_rugline', 'hb_rugline2', 'hb_washline', 'hb_crates4', 'hb_barrels', 'hb_banner']


def rows_part(game, tid, fname, maps):
    """maps: a tuple of map ids (take every sheet row those maps use) or a list of sheet rows."""
    ts = RR.tileset(game, tid)
    sheet = Image.open(os.path.join(RR.GAMES[game], 'Graphics', 'Tilesets', fname + '.png')).convert('RGBA')
    rows = set(maps) if isinstance(maps, list) else set()
    for mid in (maps if isinstance(maps, tuple) else ()):
        L, _ = RR.load(game, mid)
        rows |= {(int(t) - 384) // 8 for t in np.unique(L) if t >= 384}
    rows = sorted(r for r in rows if (r + 1) * 32 <= sheet.height)
    im = Image.new('RGBA', (256, 32 * len(rows)), (0, 0, 0, 0)); mp = {}; pas = []; pri = []
    for i, r in enumerate(rows):
        im.paste(sheet.crop((0, r * 32, 256, r * 32 + 32)), (0, i * 32))
        for c in range(8):
            src = 384 + r * 8 + c
            mp[src] = (i, c)
            pas.append(ts['passages'][src] if src < len(ts['passages']) else 0)
            pri.append(ts['priorities'][src] if src < len(ts['priorities']) else 0)
    return im, mp, pas, pri


def tint(im, hue=None, sat=1.0, val=1.0):
    a = np.array(im.convert('RGBA')).astype(np.float32); out = a.copy()
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            r, g, b, al = a[y, x]
            if al == 0: continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if hue is not None: h = hue
            r, g, b = colorsys.hsv_to_rgb(h, min(1, s * sat), min(1, v * val))
            out[y, x, :3] = (r * 255, g * 255, b * 255)
    return Image.fromarray(out.astype(np.uint8), 'RGBA')


def glyph(im, kind, col=(255, 255, 255, 235)):
    """Small shape label on a tinted drop, so no puzzle piece relies on colour alone."""
    d = ImageDraw.Draw(im)
    if kind == 'wave':
        for x0 in (6, 16):
            d.arc([x0, 12, x0 + 10, 22], 180, 360, fill=col, width=2)
    elif kind == 'leaf':
        d.polygon([(16, 8), (23, 16), (16, 24), (9, 16)], outline=col); d.line([(16, 10), (16, 26)], fill=col, width=1)
    elif kind == 'crown':
        d.polygon([(8, 22), (8, 12), (12, 17), (16, 10), (20, 17), (24, 12), (24, 22)], outline=col)
        d.line([(8, 22), (24, 22)], fill=col, width=2)
    elif kind in 'ABC':
        pts = {'A': [(11, 23), (16, 9), (21, 23)], 'B': [(11, 9), (11, 23), (20, 23), (20, 16), (11, 16), (19, 16), (19, 9), (11, 9)],
               'C': [(21, 10), (11, 10), (11, 22), (21, 22)]}[kind]
        d.line(pts, fill=col, width=2)
        if kind == 'A': d.line([(13, 18), (19, 18)], fill=col, width=2)
    return im


WOOD = [(60, 36, 24), (104, 66, 40), (146, 98, 58), (188, 138, 86)]


def post(knob, cord=None):
    """A heddle / rope post: turned timber post with a coloured grip (and a cord running up from it)."""
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([9, 25, 23, 31], fill=(0, 0, 0, 70))
    d.rectangle([13, 10, 18, 28], fill=WOOD[1]); d.line([(13, 10), (13, 28)], fill=WOOD[0]); d.line([(18, 10), (18, 28)], fill=WOOD[0])
    d.line([(15, 11), (15, 27)], fill=WOOD[3]); d.rectangle([11, 27, 20, 29], fill=WOOD[0])
    k = knob; dk = tuple(int(c * 0.6) for c in k); hl = tuple(min(255, int(c * 1.25) + 20) for c in k)
    d.rectangle([8, 5, 23, 11], fill=k, outline=dk); d.line([(10, 6), (21, 6)], fill=hl)
    if cord:
        d.line([(16, 0), (16, 5)], fill=cord, width=2)
    return im


def thread(col, kind):
    """A taut coloured thread on the floor/wall: v, h, or a corner (ne, nw, se, sw), with a knot dot for accessibility."""
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    dk = tuple(int(c * 0.55) for c in col)
    segs = {'v': [((16, 0), (16, 31))], 'h': [((0, 16), (31, 16))], 'ne': [((16, 0), (16, 16)), ((16, 16), (31, 16))],
            'nw': [((16, 0), (16, 16)), ((16, 16), (0, 16))], 'se': [((16, 31), (16, 16)), ((16, 16), (31, 16))],
            'sw': [((16, 31), (16, 16)), ((16, 16), (0, 16))]}[kind]
    for a, b in segs:
        off = (1, 0) if a[0] == b[0] else (0, 1)
        d.line([(a[0] + off[0], a[1] + off[1]), (b[0] + off[0], b[1] + off[1])], fill=dk, width=1)
        d.line([a, b], fill=col, width=1)
    return im


def warp(top=False, bottom=False):
    """Silk warp threads stretched across a loom bed (the 'gaps' of the Weaving Hall), over the dark drop."""
    im = Image.new('RGBA', (32, 32), (14, 10, 14, 255)); d = ImageDraw.Draw(im)
    for i, x in enumerate(range(2, 32, 4)):
        c = (226, 220, 204) if i % 2 == 0 else (168, 160, 150)
        d.line([(x, 0), (x, 31)], fill=c)
        d.line([(x + 1, 0), (x + 1, 31)], fill=(70, 62, 66))
    if top or bottom:                      # the breast beam the warp is tied to
        y0 = 0 if top else 22
        d.rectangle([0, y0, 31, y0 + 9], fill=WOOD[1]); d.line([(0, y0), (31, y0)], fill=WOOD[3]); d.line([(0, y0 + 9), (31, y0 + 9)], fill=WOOD[0])
        for x in range(2, 32, 4): d.point((x, y0 + 4), fill=(226, 220, 204))
    return im


def mark():
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for w, c in ((3, (40, 30, 20, 160)), (2, (250, 236, 150, 255))):
        d.line([(8, 8), (23, 23)], fill=c, width=w); d.line([(23, 8), (8, 23)], fill=c, width=w)
    return im


def treadle(up):
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([6, 12, 25, 27], fill=WOOD[1 if up else 0], outline=WOOD[0]); d.line([(8, 14), (23, 14)], fill=WOOD[3 if up else 1])
    return im


def knot(up):
    """A warp thread of Granny's Knot: raised (white, with an up-arrow head) or lowered (grey, down)."""
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = (240, 236, 220) if up else (120, 112, 120)
    d.line([(16, 2), (16, 29)], fill=c, width=2)
    if up: d.polygon([(16, 1), (9, 11), (23, 11)], fill=c, outline=(90, 80, 70))
    else: d.polygon([(16, 30), (9, 20), (23, 20)], fill=c, outline=(50, 44, 50))
    return im


def gear():
    im = Image.new('RGBA', (32, 32), (36, 30, 32, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 31, 31], outline=(20, 16, 18))
    d.ellipse([5, 5, 26, 26], fill=WOOD[1], outline=WOOD[0]); d.ellipse([12, 12, 19, 19], fill=WOOD[0])
    for a, b in (((16, 2), (16, 8)), ((16, 23), (16, 29)), ((2, 16), (8, 16)), ((23, 16), (29, 16))):
        d.line([a, b], fill=WOOD[3], width=3)
    return im


def spool():
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([7, 24, 25, 31], fill=(0, 0, 0, 70))
    d.rectangle([8, 6, 23, 9], fill=WOOD[2], outline=WOOD[0]); d.rectangle([8, 24, 23, 27], fill=WOOD[2], outline=WOOD[0])
    d.rectangle([10, 10, 21, 23], fill=(232, 226, 210), outline=(150, 142, 130))
    for y in range(12, 23, 3): d.line([(11, y), (20, y)], fill=(190, 182, 168))
    return im


def main():
    parts = []; data = {'mi': {}, 'mg': {}, 'nm': {}, 'ch': {}, 'pf': {}, 'cu': {}}
    pas = [0] * 384; pri = [0] * 384; row = 0
    tiles_by_part = {}
    for key, (game, tid, fname, maps) in (('mi', MI), ('mg', MG), ('nm', NM), ('ch', CH)):
        im, mp, p, q = rows_part(game, tid, fname, maps)
        for src, (i, c) in mp.items():
            data[key][str(src)] = 384 + (row + i) * 8 + c
            if key == 'mg' and src in SOLID_MG: p[i * 8 + c] = 15
        parts.append(im); pas += p; pri += q; row += im.height // 32; tiles_by_part[key] = im
    # pf props, tile by tile from the PF Rejuv sheet
    reg = json.load(open(REG)); t50 = next(t for t in reg if t['id'] == 50)
    pfs = Image.open(os.path.join(OUT, 'Graphics', 'Tilesets', 'PF Rejuv.png')).convert('RGBA')
    st = json.load(open(os.path.join(HERE, 'data', 'stamps_rjc.json')))
    ids = sorted({int(t) for n in PF_STAMPS for t in np.array(st[n]['layers']).reshape(-1) if t})
    cells = []
    for t in ids:
        k = t - 384; cells.append((pfs.crop((k % 8 * 32, k // 8 * 32, k % 8 * 32 + 32, k // 8 * 32 + 32)), 15 if t in SOLID_PF else t50['passages'][t], t50['priorities'][t], ('pf', str(t))))

    def src(key, sid):
        nid = data[key][str(sid)] - 384; imall = Image.new('RGBA', (256, sum(p.height for p in parts)))
        y = 0
        for p in parts: imall.paste(p, (0, y)); y += p.height
        return imall.crop((nid % 8 * 32, nid // 8 * 32, nid % 8 * 32 + 32, nid // 8 * 32 + 32))

    def add(name, im, p=0, q=0): cells.append((im, p, q, ('cu', name)))
    RED, GOLD, GREEN, BRASS, WHITE = (214, 64, 64), (236, 190, 60), (70, 176, 96), (190, 150, 70), (236, 232, 220)
    COLS = {'red': RED, 'gold': GOLD, 'green': GREEN, 'brass': BRASS, 'silk': WHITE, 'blue': (90, 176, 240)}
    plank = src('mi', 962)
    add('plank', plank)                                             # walkable board across a loom bed
    add('warp', warp(), 15); add('warp_top', warp(top=True), 15); add('warp_bot', warp(bottom=True), 15)
    for n, c in COLS.items():
        add('post_' + n, post(c, c), 15)
        for k in ('v', 'h', 'ne', 'nw', 'se', 'sw'): add('thread_%s_%s' % (n, k), thread(c, k), 0 if n in ('silk', 'brass') else 15)  # coloured strands hang over drops
    add('mark', mark())
    add('treadle_up', treadle(True), 15); add('treadle_down', treadle(False), 15)
    add('knot_up', knot(True), 15); add('knot_down', knot(False), 15)
    add('gear', gear(), 15); add('spool', spool(), 15)
    # scenery drops: the theatre's own curtain tiles re-dyed, each with a shape label (wave / leaf / crown)
    for n, hue, g in (('ship', 0.58, 'wave'), ('forest', 0.33, 'leaf'), ('throne', 0.13, 'crown')):
        add('drop_%s_top' % n, tint(src('mg', 4681), hue, 0.9, 1.0), 15)
        add('drop_%s' % n, glyph(tint(src('mg', 4689), hue, 0.9, 1.0), g), 15)
        add('drop_%s_bot' % n, tint(src('mg', 4697), hue, 0.9, 1.0), 15)
    for n in 'ABC':                                                  # loft flats: grey canvas, lettered
        add('flat_%s' % n, glyph(tint(src('mg', 4689), 0.08, 0.25, 1.15), n, (60, 40, 30, 255)), 15)
        add('flat_%s_hung' % n, glyph(tint(src('mg', 4689), 0.08, 0.25, 0.8), n, (240, 230, 200, 255)), 15)
    add('gangplank', tint(plank, 0.58, 0.5, 1.1)); add('log', tint(plank, 0.09, 1.1, 0.8)); add('dais', tint(plank, 0.0, 1.2, 1.0))
    add('rostrum', tint(plank, 0.13, 0.9, 1.25))
    # ---- art pass (2026-11-19): the Playhouse's proscenium, painted drop, footlights and orchestra pit; the Weaving
    # Hall's depth under the loom beds (hall_art.py, drawn on the 16-px grid and doubled like the tiles around them)
    import hall_art as HA
    for (cx, cy), t in HA.tiles(HA.backdrop(15, 3)).items(): add('backdrop_%d_%d' % (cx, cy), t, 15)
    for p in ('cap', 'shaft', 'base'): add('column_' + p, HA.gold_column(p), 15)
    for p in ('l', 'mid', 'r'): add('beam_' + p, HA.proscenium_beam(p), 15)
    for (cx, cy), t in HA.tiles(HA.mask_crest()).items(): add('crest_%d' % cx, t, 15)
    add('footlight', HA.footlight(), 15); add('glow', HA.glow(), 0)
    for (cx, cy), t in HA.tiles(HA.old_poster()).items(): add('paste_%d_%d' % (cx, cy), t, 15)
    for i, f in enumerate((1241, 1242, 1243)): add('pit_%d' % i, HA.pit_floor(src('mi', f)), 15)
    for p in ('l', 'mid', 'r'): add('pit_rail_' + p, HA.pit_rail(p), 15)
    add('music_stand', HA.music_stand(), 15)
    for p in ('l', 'mid', 'r'): add('loom_face_' + p, HA.loom_face(p), 15)
    for n in ('red', 'gold', 'green'): add('loom_face_' + n, HA.loom_face('mid', COLS[n]), 15)
    for dpt in range(4):
        for i, f in enumerate((1241, 1242, 1243)): add('lower_%d_%d' % (dpt, i), HA.lower_floor(src('mi', f), dpt), 15)
    add('warp_mid', HA.warp_overlay('mid'), 15); add('warp_back', HA.warp_overlay('bot'), 15)
    for k in ('full', 'l', 'r'):
        add('light_' + k, HA.light(k), 0)                          # on walkable boards
        add('light_%s_x' % k, HA.light(k), 15)                     # over a loom bed (keeps it solid)
    for p in ('mid', 'band', 'base'): add('tpost_' + p, HA.post(p), 15)
    for p in ('top', 'mid', 'sill'):
        for (cx, cy), t in HA.tiles(HA.window(p)).items(): add('window_%s_%d' % (p, cx), t, 15)
    for n in ('red', 'gold', 'green', 'silk'):
        add('heddle_%s_top' % n, HA.heddle_frame(COLS[n], 'top'), 0, 1)   # the frame's header, drawn over the walker
        add('heddle_%s_bot' % n, HA.heddle_frame(COLS[n], 'bot'), 15)
    for n, c in (('bolt_r', (170, 50, 60)), ('bolt_b', (60, 90, 170)), ('bolt_y', (200, 160, 60)), ('bolt_p', (150, 70, 150))):
        add(n, HA.dim(HA.silk_bolt(c)), 15)
    add('basket', HA.dim(HA.yarn_basket([RED, GOLD, GREEN])), 15)
    for n in ('hb_crates4', 'hb_barrels', 'pf_p_silk', 'pf_p_vat_b', 'pf_p_vat_r', 'pf_p_vat_y'):   # props on the floor below, dimmed
        for t in sorted({int(t) for t in np.array(st[n]['layers']).reshape(-1) if t}):
            k = t - 384; add('dim_%d' % t, HA.dim(pfs.crop((k % 8 * 32, k // 8 * 32, k % 8 * 32 + 32, k // 8 * 32 + 32))), 15)
    # ---- the Canopy (Gym 2 redo, SPINE Rev 19): the hollow of Briarwick's elder tree, webs strung across the drop
    for dpt in range(3):
        for sd in range(3): add('hollow_%d_%d' % (dpt, sd), HA.hollow(dpt, sd), 15)
    for p in ('l', 'mid', 'r'): add('ledge_face_' + p, HA.ledge_face(p), 15)
    for sd in range(4): add('root_%d' % sd, HA.root(sd), 15)
    add('web_taut', HA.web('taut'), 0); add('web_sticky', HA.web('sticky'), 0)        # webs are events; the tiles are walkable
    add('web_anchor_l', HA.web_anchor('l'), 15); add('web_anchor_r', HA.web_anchor('r'), 15)
    for p in ('tl', 'tr', 'bl', 'br'): add('knot_hole_' + p, HA.knot_hole(p), 15)
    for nm_, t in (('cocoon_top', 17752), ('cocoon_bot', 17753), ('strand_w_top', 17755), ('strand_w_bot', 17757),
                   ('strand_p_top', 17754), ('strand_p_bot', 17756)):     # silk cocoons and dyed lengths hung over the drop: solid copies
        k = t - 384; add(nm_, pfs.crop((k % 8 * 32, k // 8 * 32, k % 8 * 32 + 32, k // 8 * 32 + 32)), 15)
    for t in BARK:                                                  # the elder's bark, for the hollow's walls (PF Rejuv pf part)
        k = t - 384; tile = pfs.crop((k % 8 * 32, k // 8 * 32, k % 8 * 32 + 32, k // 8 * 32 + 32))
        add('bark_%d' % t, tile, 15); add('bark_dim_%d' % t, HA.trunk_side(tile), 15)
    cu = Image.new('RGBA', (256, 32 * ((len(cells) + 7) // 8)), (0, 0, 0, 0))
    for i, (im, p, q, (key, name)) in enumerate(cells):
        cu.paste(im, (i % 8 * 32, i // 8 * 32)); data[key][name] = 384 + row * 8 + i
    n = cu.height // 32 * 8
    pas += [c[1] for c in cells] + [0] * (n - len(cells)); pri += [c[2] for c in cells] + [0] * (n - len(cells))
    parts.append(cu)
    sheet = Image.new('RGBA', (256, sum(p.height for p in parts)), (0, 0, 0, 0)); y = 0
    for p in parts: sheet.paste(p, (0, y)); y += p.height
    os.makedirs(os.path.join(OUT, 'Graphics', 'Tilesets'), exist_ok=True)
    sheet.save(os.path.join(OUT, 'Graphics', 'Tilesets', NAME + '.png'))
    e = dict(id=TID, name=NAME, tileset_name=NAME, autotile_names=[''] * 7, panorama='', fog='', battleback='',
             n_tiles=len(pas), passages=pas, priorities=pri, terrain_tags=[0] * len(pas))
    reg = [t for t in json.load(open(REG)) if t['id'] != TID] + [e]          # re-read: other composers share this registry
    json.dump(sorted(reg, key=lambda t: t['id']), open(REG, 'w'))
    data['ranges'] = {'mi': [384, 384 + tiles_by_part['mi'].height // 32 * 8 - 1],
                      'mg': [384 + tiles_by_part['mi'].height // 32 * 8, 384 + (tiles_by_part['mi'].height + tiles_by_part['mg'].height) // 32 * 8 - 1]}
    json.dump(data, open(os.path.join(HERE, 'data', 'halls.json'), 'w'))
    print('tileset %d %s: %d tiles, sheet 256x%d (mi %d rows, mg %d rows, own %d tiles)' % (
        TID, NAME, len(pas) - 384, sheet.height, tiles_by_part['mi'].height // 32, tiles_by_part['mg'].height // 32, len(cells)))


if __name__ == '__main__':
    main()
