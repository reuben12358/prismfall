"""backstrips.py - show back-sprite strips frame by frame at native density (x K), bottom-aligned, for donor picking.
python3 -I tools/kitbash/backstrips.py OUT.png K spec [spec ...]
spec: EB:<name> (base project Graphics/Trainers/<name>.png), RB:/RJ:/DS:<trbackNNN>, HG:<NAME_back>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image, ImageDraw

PATHS = {'EB': '/home/claude/ref/ebdx/Graphics/Trainers/%s.png',
         'RB': '/home/claude/ref/games/reborn/Graphics/Characters/%s.png',
         'RJ': '/home/claude/ref/games/rejuvenation/Graphics/Characters/%s.png',
         'DS': '/home/claude/ref/games/desolation/Graphics/Characters/%s.png',
         'HG': '/home/claude/ref/art/sprites_gen4_partner_backs/extracted/HGSS Partner Backsprites/%s.png'}


def frames(spec, n=5):
    s, name = spec.split(':', 1)
    im = kb.load(PATHS[s] % name)
    w, h = im.size
    if w < 3 * h:
        n = 1
    fw = w // n
    out = []
    for i in range(n):
        fr = im.crop((i * fw, 0, (i + 1) * fw, h))
        # halve: these strips are doubled but some sit at odd offsets, so sample the phase with the most uniform blocks
        best = None
        for ox in (0, 1):
            for oy in (0, 1):
                c = fr.crop((ox, oy, ox + (fw - ox) // 2 * 2, oy + (h - oy) // 2 * 2))
                r = kb.doubled_ratio(c)
                if best is None or r > best[0]:
                    best = (r, c)
        c = best[1]
        out.append(c.resize((c.size[0] // 2, c.size[1] // 2), Image.NEAREST))
    return out


def main(out, k, specs):
    rows = []
    for sp in specs:
        frs = frames(sp)
        rows.append((sp, frs))
    mh = max(f.size[1] for _, frs in rows for f in frs)
    mw = max(f.size[0] for _, frs in rows for f in frs)
    W = 5 * (mw * k + 6) + 140
    H = len(rows) * (mh * k + 8)
    sh = Image.new('RGBA', (W, H), (40, 42, 50, 255)); d = ImageDraw.Draw(sh)
    y = 0
    for sp, frs in rows:
        d.text((4, y + 4), sp, fill=(230, 230, 230, 255), font=kb.font(11))
        for i, f in enumerate(frs):
            z = kb.up(kb.on_bg(f, (150, 160, 170, 255)), k)
            sh.alpha_composite(z, (140 + i * (mw * k + 6), y + mh * k - z.size[1]))
        y += mh * k + 8
    sh.save(out); print(out, sh.size)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3:])
