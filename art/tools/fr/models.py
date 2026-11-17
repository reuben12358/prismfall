from exprs import Face
from fs import hx

GL = '#4e4860'


def larch_post(f, expr):
    # age: eye bags and laugh lines (mid skin), drawn before glasses
    sk1 = f.sk[1]
    for x in range(34, 45):
        if f.is_skin(x, 51):
            f.put(x, 51, sk1)
    for x, y in ((48, 53), (47, 54), (47, 55), (46, 56), (58, 54), (59, 55)):
        if f.is_skin(x, y):
            f.put(x, y, sk1)
    # reading glasses (low on the nose) + chain
    f.thick([(31, 38), (47, 38), (47, 47), (31, 47), (31, 38)], c=GL, w=1)
    f.thick([(57, 38), (69, 38), (69, 47), (57, 47)], c=GL, w=1)
    f.thick([(47, 40), (52, 39), (57, 40)], c=GL, w=1)
    for (x, y) in ((33, 40), (34, 41), (59, 40), (60, 41)):
        f.put(x, y, '#e8f0f8')
    for i, (x, y) in enumerate([(31, 49), (30, 52), (29, 55), (28, 58), (28, 61), (28, 64), (29, 67), (30, 70)]):
        f.put(x, y, '#c8a848' if i % 2 == 0 else '#8a7030')
    # braid over the near shoulder: tapered band, alternating plaits
    import math
    H = ['#4a4858', '#6e6c7c', '#9a9aaa', '#c8c8d4']
    P0, P1 = (27.0, 61.0), (16.0, 93.0)
    L = math.hypot(P1[0] - P0[0], P1[1] - P0[1])
    ax, ay = (P1[0] - P0[0]) / L, (P1[1] - P0[1]) / L
    for y in range(56, 96):
        for x in range(4, 40):
            px_, py_ = x + 0.5 - P0[0], y + 0.5 - P0[1]
            v = px_ * ax + py_ * ay
            u = -px_ * ay + py_ * ax
            if v < -1 or v > L:
                continue
            half = 5.0 - 1.4 * v / L
            k = int(v // 5.2); s_ = 1 if k % 2 else -1; vv = v - k * 5.2
            if abs(u) <= half:
                q = vv + u * s_ * 0.9
                if vv < 0.9:
                    c = H[0]
                elif 1.2 < q < 3.0:
                    c = H[3]
                elif q < 4.4:
                    c = H[2]
                else:
                    c = H[1]
                if abs(u) > half - 1.0 and c in (H[2], H[3]):
                    c = H[1]
                f.put(x, y, c)
            elif abs(u) <= half + 1.2:
                f.put(x, y, f.line)
    for y in range(91, 95):
        for x in range(12, 20):
            f.put(x, y, '#a8453a' if y < 94 else f.line)
    for x in range(12, 20):
        f.put(x, 90, f.line)


MODELS = {
    'PLAYER_A': dict(base='pca', skin=['#a07040', '#d8a888', '#f8d8c0'], iris=['#1e6a68', '#2f948c'],
                     hair=['#363244', '#5a566c', '#8a84a2'], eyes=[(24, 43, 36, 55), (50, 42, 64, 54)],
                     brows=[(24, 35, 39), (63, 51, 38)], mouth=(38, 66, 60, 75), forehead=(32, 26, 58, 36),
                     neutral_mouth='smile', happy_mouth='shout'),
    'PLAYER_B': dict(base='pcb', skin=['#c48474', '#d8a888', '#f8d8c0'], iris=['#1e6a68', '#3fa69e'], iris_extra=['#c8c8d8'],
                     hair=['#5a2a44', '#8e4c68', '#b87892'], eyes=[(20, 31, 34, 54), (50, 34, 64, 54)],
                     brows=[(20, 33, 28), (63, 51, 30)], mouth=(36, 61, 53, 69), forehead=(30, 20, 60, 28),
                     neutral_mouth='smile', happy_mouth='shout'),
    'LARCH': dict(base='larch', skin=['#a07040', '#d8a888', '#f8d8c0'], iris=['#2c4048', '#56707a'],
                  hair=['#6a6878', '#9898a8', '#d8d8e2'], eyes=[(32, 32, 46, 48), (60, 32, 68, 48)],
                  brows=[(32, 45, 28), (68, 61, 28)], mouth=(42, 56, 58, 64), forehead=(38, 18, 66, 26),
                  neutral_mouth='flat', happy_mouth='shout', post=larch_post),
}
