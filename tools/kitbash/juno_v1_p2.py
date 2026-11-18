"""Juno V1 "Under Glass" - PASS 2. python3 -I tools/kitbash/juno_v1_p2.py
Changes vs pass 1: deeper brass ramp with shade under every member, glass cut to a few flat tints,
leather harness band round the case + her cast shadow on the glass, ponytail swapped for Sonia's
curled side-ponytail (sd:sonia, flipped so the head angle matches)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show, wardian2
import juno_v1_underglass as v1
from mat import H, BLACK, CLEAR
from PIL import Image

OUT = kb.WORK + '/passes'
LEATHER = [H('3e2014'), H('6e3e24'), H('9a6038'), H('c48a54')]


def case():
    wardian2.BR_D, wardian2.BR_M, wardian2.BR_L, wardian2.BR_H = H('5a3410'), H('9a6a20'), H('d8a840'), H('fbe698')
    wardian2.GLASS = {'side': (H('c8ece4'), H('a4d6d0')), 'roof': (H('def6ee'), H('c8ece4')), 'front': (H('8ccac6'), H('64a8ac'))}
    fx0, fx1, eave, base = 14, 42, 21, 43
    c, _ = wardian2.build(fx0=fx0, fx1=fx1, ncol=22)
    p = c.load()
    # her cast shadow on the glass next to her back (2 columns), brass kept
    brass = {wardian2.BR_D, wardian2.BR_M, wardian2.BR_L, wardian2.BR_H, BLACK}
    for y in range(eave - 8, base):
        for x in (fx1 - 3, fx1 - 2):
            if p[x, y][3] and p[x, y] not in brass:
                p[x, y] = H('4a8890') if kb.lum(p[x, y]) > 120 else H('2c5a64')
    # leather harness band round the case under the eave (3 px: light, mid, dark) with a brass buckle
    for x in range(fx0 - 4, fx1 + 1):
        yy = eave + 5 + (0 if x >= fx0 else -(fx0 - x) // 2)
        for k, col in enumerate([LEATHER[2], LEATHER[1]]):
            if p[x, yy + k][3]:
                p[x, yy + k] = col
    for (x, y, col) in [(fx0 + 6, eave + 5, wardian2.BR_H), (fx0 + 7, eave + 5, wardian2.BR_L), (fx0 + 6, eave + 6, wardian2.BR_L),
                        (fx0 + 7, eave + 6, LEATHER[0]), (fx0 + 5, eave + 5, wardian2.BR_M), (fx0 + 5, eave + 6, wardian2.BR_D)]:
        p[x, y] = col
    return mat.shear_rows(c, 49, 5)


def sonia_tail():
    n, f = show.get_native('sd:sonia')
    t = n.crop((44, 0, 62, 25))
    hair = [(105, 41, 32, 255), (194, 73, 39, 255), (184, 92, 69, 255), (240, 147, 114, 255), (247, 163, 138, 255),
            (254, 180, 130, 255), (219, 242, 231, 255), (198, 227, 231, 255), (255, 255, 255, 255)]
    ramp = [H('5a2418'), H('a8442a'), H('c05a32'), H('e07a44'), H('e07a44'), H('f0a060'), H('fbd09a'), H('fbd09a'), H('fbd09a')]
    keep = set(hair) | {BLACK}
    p = t.load()
    for y in range(t.size[1]):
        for x in range(t.size[0]):
            if p[x, y][3] and p[x, y] not in keep:
                p[x, y] = CLEAR
    t = mat.recolour(t, dict(zip(hair, ramp)))
    t = mat.clean_orphans(t)
    return mat.flip(t)


def compose(tx=31, ty=3):
    b, body, pack = v1.stage_cut()
    body = v1.stage_recolour(body)
    # 2-tone leather strap on her chest
    reg = mat.region(body.size, [[(36, 2), (50, 2), (50, 12), (47, 14), (45, 16), (36, 16)]])
    body = mat.erase(body, reg)
    body = mat.under(body, sonia_tail(), tx, ty)
    return mat.under(body, case(), 0, 0)


if __name__ == '__main__':
    out = compose()
    out.save(OUT + '/v1_p2.png')
    kb.contact([('p2', out.crop((6, 0, 70, 52)))], 1, (64 * 8, 52 * 8), k=8).save(kb.WORK + '/sheets/v1_p2_8x.png')
