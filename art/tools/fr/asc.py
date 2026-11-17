"""ASCII pixel grids: dump a stock sprite as text (pose skeleton), and load
hand-drawn character grids back to RGBA.  Grid files: a 'legend' block of
`c = #rrggbb` lines, then '---', then rows ('.' = transparent)."""
import numpy as np
from fs import hx, palette

SYMS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def dump(a, x0=0, y0=0, x1=None, y1=None):
    x1 = a.shape[1] - 1 if x1 is None else x1
    y1 = a.shape[0] - 1 if y1 is None else y1
    pal = [c for c, n, bb in palette(a)]
    sym = {c: SYMS[i] for i, c in enumerate(pal)}
    lines = ['legend: ' + ' '.join(f'{sym[c]}=#{c[0]:02x}{c[1]:02x}{c[2]:02x}' for c in pal)]
    lines.append('    ' + ''.join(str((x // 10) % 10) for x in range(x0, x1 + 1)))
    lines.append('    ' + ''.join(str(x % 10) for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        row = ''.join(sym[tuple(int(v) for v in a[y, x, :3])] if a[y, x, 3] else '.' for x in range(x0, x1 + 1))
        lines.append(f'{y:3d} ' + row)
    return '\n'.join(lines)


def load_grid(path, w=64, h=64):
    txt = open(path).read()
    head, body = txt.split('\n---\n', 1)
    legend = {}
    for line in head.splitlines():
        line = line.split('#', 1)[0] if line.strip().startswith('#') else line
        if '=' in line:
            k, v = line.split('=', 1)
            legend[k.strip()] = v.strip()
    rows = [r for r in body.splitlines() if r.strip() != '']
    a = np.zeros((h, w, 4), np.uint8)
    for y, r in enumerate(rows[:h]):
        r = r.split('|')[-1] if '|' in r else r
        for x, ch in enumerate(r[:w]):
            if ch in '. ':
                continue
            a[y, x, :3] = hx(legend[ch]); a[y, x, 3] = 255
    return a
