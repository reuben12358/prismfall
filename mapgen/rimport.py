#!/usr/bin/env python3
"""rimport.py - pieces imported from the NEW_SOURCES.md sheets (16-px art with a baked checker background).

The checker is keyed out by a flood fill from the sheet border through pixels that equal the expected checker colour
at their position, so white snow inside an outline survives.  Pieces are cropped, padded to the 16-px grid (bottom
aligned) and saved at 1x in data/imports/ with a manifest; rdraw.pieces_late() hands them to rcustom.py, which doubles
them by exactly 2x (nearest neighbour) like every drawn piece.  The source folder is read-only reference data.

    python3 -I rimport.py && python3 -I rcustom.py && python3 -I rcompose.py && python3 -I rstamps.py

Imported: carchagui "Snow village tiles" chalets (credit carchagui).  Looked at and NOT imported: Magiscarf's
snow-capped trees ("Bunch o' free tiles"): flat scale-leaf shading and saturated greens beside the Sheridan-derived
snow lattice read as another game (style test 2026-11-19)."""
import os, sys, json
from collections import deque, Counter
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
REF = '/home/claude/ref/assets'
OUT = os.path.join(HERE, 'data', 'imports')
# name: (sheet, box x0 y0 x1 y1, pad left px, door column, credit)
PIECES = {
    'ch_chalet_a': ('da_carchagui/Snow village tiles.png', (17, 16, 127, 144), 1, 3, 'carchagui'),
    'ch_chalet_b': ('da_carchagui/Snow village tiles.png', (145, 33, 255, 144), 1, 3, 'carchagui'),
    'ch_chalet_c': ('da_carchagui/Snow village tiles.png', (273, 33, 383, 144), 1, 3, 'carchagui'),
    'ch_chalet_pc': ('da_carchagui/Snow village tiles.png', (17, 176, 168, 304), 2, 3, 'carchagui'),
    'ch_chalet_shop': ('da_carchagui/Snow village tiles.png', (177, 176, 311, 304), 2, 2, 'carchagui'),
}


def key(path):
    im = np.array(Image.open(path).convert('RGB')).astype(int); H, W, _ = im.shape
    (c1, _), (c2, _) = Counter(map(tuple, im.reshape(-1, 3))).most_common(2)
    best = None
    yy, xx = np.mgrid[0:H, 0:W]
    for s in (8, 16):
        par = ((xx // s) + (yy // s)) % 2
        for a, b in ((c1, c2), (c2, c1)):
            exp = np.where(par[..., None] == 0, np.array(a), np.array(b))
            m = (im == exp).all(-1).mean()
            if best is None or m > best[0]: best = (m, exp)
    bg = (im == best[1]).all(-1)
    seen = np.zeros((H, W), bool); q = deque()
    for x in range(W):
        for y in (0, H - 1):
            if bg[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(H):
        for x in (0, W - 1):
            if bg[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            Y, X = y + dy, x + dx
            if 0 <= Y < H and 0 <= X < W and bg[Y, X] and not seen[Y, X]: seen[Y, X] = True; q.append((Y, X))
    return Image.fromarray(np.dstack([im, np.where(seen, 0, 255)]).astype(np.uint8), 'RGBA')


def main():
    os.makedirs(OUT, exist_ok=True)
    sheets = {}; man = {}
    for n, (sheet, box, padl, door, credit) in PIECES.items():
        if sheet not in sheets: sheets[sheet] = key(os.path.join(REF, sheet))
        t = sheets[sheet].crop(box)
        w = -(-(t.width + padl) // 16); h = -(-t.height // 16)
        im = Image.new('RGBA', (w * 16, h * 16), (0, 0, 0, 0)); im.alpha_composite(t, (padl, h * 16 - t.height))
        im.save(os.path.join(OUT, n + '.png'))
        code = ['R' * w] + ['r' * w] * (h - 3) + ['W' * w, ''.join('D' if c == door else 'W' for c in range(w))]
        man[n] = dict(w=w, h=h, code=code, door=[door, h - 1], source=sheet, credit=credit)
    json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
    print('imports', {n: (v['w'], v['h']) for n, v in man.items()})


if __name__ == '__main__':
    main()
