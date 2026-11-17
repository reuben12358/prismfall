"""Expression edits on hand-drawn 96px busts.  Each face has a model:
eye boxes, brow row, mouth box, skin/line colours.  Ops only touch those
regions; everything else stays the original hand-drawn art."""
import numpy as np
from PIL import Image
from fs import hx, rect
import busts

EXPRS = ['neutral', 'happy', 'smug', 'angry', 'crying', 'shocked', 'deadpan', 'panic', 'sad', 'blush']


class Face:
    def __init__(self, a, m):
        self.a = a.copy()
        self.m = m
        self.line = hx(m.get('line', '#181820'))
        self.sk = [hx(c) for c in m['skin']]          # [dark, mid, light]

    # ---------------------------------------------------------- helpers
    def put(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < 96 and 0 <= y < 96:
            self.a[y, x, :3] = hx(c); self.a[y, x, 3] = 255

    def thick(self, pts, c=None, w=2):
        c = self.line if c is None else c
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for k in range(n + 1):
                x = x0 + (x1 - x0) * k / n; y = y0 + (y1 - y0) * k / n
                for dx in range(w):
                    for dy in range(w):
                        self.put(x + dx - (w - 1) / 2, y + dy - (w - 1) / 2, c)

    def is_skin(self, x, y):
        return tuple(self.a[y, x, :3]) in self.sk and self.a[y, x, 3] > 0

    def erase(self, box, keep=()):
        """Repaint non-skin pixels in box from the nearest skin pixel in the
        same row (keeps the hand-drawn horizontal shading bands)."""
        x0, y0, x1, y1 = box
        src = self.a.copy()
        keep = [hx(k) for k in keep]
        for y in range(max(0, y0), min(96, y1 + 1)):
            for x in range(max(0, x0), min(96, x1 + 1)):
                c = tuple(src[y, x, :3])
                if (c in self.sk and src[y, x, 3] > 0) or c in keep or src[y, x, 3] == 0:
                    continue
                best = None
                for r in range(1, 20):
                    for xx, yy in ((x - r, y), (x + r, y), (x, y - r), (x, y + r)):
                        if 0 <= xx < 96 and 0 <= yy < 96 and not (x0 <= xx <= x1 and y0 <= yy <= y1 and tuple(src[yy, xx, :3]) not in self.sk):
                            cc = tuple(src[yy, xx, :3])
                            if cc in self.sk and src[yy, xx, 3] > 0:
                                best = cc; break
                    if best:
                        break
                if best:
                    self.a[y, x, :3] = best; self.a[y, x, 3] = 255

    # ---------------------------------------------------------- eyes
    def eye_closed(self, box, shape):
        self.erase(box)
        x0, y0, x1, y1 = box
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + self.m.get('lid_dy', 0)
        hw = (x1 - x0) / 2 - 1
        if shape == '^':
            self.thick([(cx - hw, cy + 3), (cx - hw / 2, cy - 1), (cx, cy - 2), (cx + hw / 2, cy - 1), (cx + hw, cy + 3)])
        elif shape == 'u':
            self.thick([(cx - hw, cy), (cx - hw / 2, cy + 3), (cx + hw / 2, cy + 3), (cx + hw, cy)])
        elif shape in '><':
            s = 1 if shape == '>' else -1
            tip = cx + s * hw * 0.8
            self.thick([(cx - s * hw, cy - 4), (tip, cy), (cx - s * hw, cy + 4)])
        elif shape == '-':
            self.thick([(cx - hw, cy + 1), (cx + hw, cy + 1)])

    def lid(self, box, frac, line_w=2):
        """Lower the upper lid: skin above, a lash line at the new edge."""
        x0, y0, x1, y1 = box
        cut = int(y0 + (y1 - y0) * frac)
        ys, xs = [], []
        for y in range(y0, cut + 1):
            for x in range(x0, x1 + 1):
                c = tuple(self.a[y, x, :3])
                if not self.is_skin(x, y) and self.a[y, x, 3] > 0 and c not in self.m.get('hair', []):
                    ys.append(y); xs.append(x)
        if not xs:
            return
        self.erase((x0, y0, x1, cut), keep=self.m.get('hair', []))
        self.thick([(min(xs), cut), (max(xs), cut)], w=line_w)

    def pupils_small(self, box, white='#f0f0f8', look=0):
        x0, y0, x1, y1 = box
        W = hx(white)
        line = self.line
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = tuple(self.a[y, x, :3])
                inner = x0 + 2 <= x <= x1 - 2 and y0 + 3 <= y <= y1 - 2
                if c in [hx(i) for i in self.m['iris']] or c == hx(self.m.get('shine', '#f0f0f8')) or (inner and c == self.line) \
                        or c in [hx(i) for i in self.m.get('iris_extra', [])]:
                    self.a[y, x, :3] = W
        cx = (x0 + x1) / 2 + look
        cy = (y0 + y1) / 2 + 1
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1, 2):
                if abs(dx) + abs(dy) < 3:
                    self.put(cx + dx, cy + dy, line)

    def eye_white_ring(self, box):
        """Panic: eye becomes a white disc with a dot."""
        x0, y0, x1, y1 = box
        self.erase(box)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if d <= 0.62:
                    self.put(x, y, '#f8f8fc')
                elif d <= 1.0:
                    self.put(x, y, self.line)
        self.put(cx, cy, self.line); self.put(cx - 1, cy, self.line)

    # ---------------------------------------------------------- brows
    def brow(self, side, inner_dy, outer_dy, lift=0):
        b = self.m['brows'][side]          # (x_outer, x_inner, y)
        xo, xi, y = b
        y -= lift
        self.erase((min(xo, xi) - 1, y - 6, max(xo, xi) + 1, y + 2), keep=self.m.get('hair', []))
        pts = [(xo, y + outer_dy), (xi, y + inner_dy)]
        hair = [hx(h) for h in self.m.get('hair', [])]
        n = int(abs(xi - xo)) * 2 + 1
        for k in range(n + 1):
            x = xo + (xi - xo) * k / n; yy = y + outer_dy + (inner_dy - outer_dy) * k / n
            for dy in (0, 1):
                X, Y = int(round(x)), int(round(yy + dy))
                if 0 <= X < 96 and 0 <= Y < 96 and tuple(self.a[Y, X, :3]) not in hair:
                    self.put(X, Y, self.line)

    # ---------------------------------------------------------- mouth
    def mouth(self, kind):
        x0, y0, x1, y1 = self.m['mouth']
        # lip shading uses the darkest skin tone: treat it as erasable here
        sk = self.sk
        self.sk = sk[1:]
        self.erase((x0, y0, x1, y1))
        self.sk = sk
        cx, cy = (x0 + x1) / 2 + self.m.get('mouth_dx', 0), (y0 + y1) / 2
        L = self.line
        inside = '#7a2c38'; tongue = '#d86a70'; teeth = '#f4f4f8'
        if kind == 'line':
            self.thick([(cx - 4, cy), (cx + 3, cy)], w=1); self.thick([(cx - 3, cy + 1), (cx + 2, cy + 1)], c=self.sk[1], w=1)
        elif kind == 'smile':
            self.thick([(cx - 6, cy - 2), (cx - 3, cy + 1), (cx + 3, cy + 1), (cx + 5, cy - 2)], w=1)
            self.thick([(cx - 3, cy + 2), (cx + 2, cy + 2)], c=self.sk[1], w=1)
        elif kind == 'frown':
            self.thick([(cx - 5, cy + 2), (cx - 2, cy), (cx + 2, cy), (cx + 5, cy + 2)], w=1)
        elif kind == 'flat':
            self.thick([(cx - 5, cy), (cx + 5, cy)], w=1)
        elif kind == 'smirk':
            self.thick([(cx - 5, cy + 1), (cx + 1, cy + 1), (cx + 5, cy - 2), (cx + 6, cy - 3)], w=1)
            self.put(cx + 7, cy - 4, self.sk[1])
        elif kind in ('o', 'shout', 'wail', 'grit', 'wobble'):
            if kind == 'o':
                rx, ry = 3, 4
            elif kind == 'shout':
                rx, ry = 6, 4
            elif kind == 'wail':
                rx, ry = 8, 6
            else:
                rx, ry = 7, 3
            for y in range(int(cy - ry - 1), int(cy + ry + 2)):
                for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                    d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                    if kind in ('grit', 'wobble'):
                        d = max(abs(x + 0.5 - cx) / rx, abs(y + 0.5 - cy) / ry) ** 2
                    if d <= 1.0:
                        c = inside
                        if kind in ('grit', 'wobble'):
                            c = teeth
                        elif kind in ('shout', 'wail') and y < cy - ry + 2:
                            c = teeth
                        elif kind in ('shout', 'wail') and y > cy + ry - 3:
                            c = tongue
                        self.put(x, y, c)
                    elif d <= 1.5:
                        self.put(x, y, L)
            if kind == 'grit':
                self.thick([(cx - rx, cy), (cx + rx, cy)], c='#b8b8c8', w=1)
                for x in range(int(cx - rx + 2), int(cx + rx), 3):
                    self.put(x, cy - 1, '#b8b8c8'); self.put(x, cy + 1, '#b8b8c8')
            if kind == 'wobble':
                self.thick([(cx - rx, cy), (cx - rx / 2, cy - 1), (cx, cy + 1), (cx + rx / 2, cy - 1), (cx + rx, cy)], c=L, w=1)
        elif kind == 'wavy':
            self.thick([(cx - 5, cy), (cx - 3, cy - 1), (cx - 1, cy + 1), (cx + 1, cy - 1), (cx + 3, cy + 1), (cx + 5, cy)], w=1)
        elif kind == 'keep':
            pass

    # ---------------------------------------------------------- extras
    def tears(self):
        for (x0, y0, x1, y1) in self.m['eyes']:
            cx = (x0 + x1) / 2
            for y in range(y1 - 2, min(95, y1 + 22)):
                w = 2 if y < y1 + 14 else 1
                for dx in range(w + 1):
                    self.put(cx - 2 + dx, y, '#a8dcf8' if dx else '#e4f4ff')
            self.thick([(x0, y1 - 1), (x1, y1 - 1)], c='#a8dcf8', w=1)

    def blush(self, strong=False):
        for (x0, y0, x1, y1) in self.m['eyes']:
            cy = y1 + 4
            for i in range(3 if not strong else 4):
                x = x0 + 2 + i * 4
                self.thick([(x, cy + 3), (x + 2, cy)], c='#e8788a', w=1)

    def gloom(self):
        x0, y0, x1, y1 = self.m['forehead']
        for x in range(x0, x1 + 1, 3):
            for y in range(y0, y1 + 1):
                if self.is_skin(x, y):
                    self.put(x, y, '#8a90c8')

    def sweat(self):
        x, y = self.m.get('sweat', (80, 30))
        for dy, row in enumerate([".k.", "kbk", "kbk", "kwbk"[:3], ".k."]):
            pass


def apply(base, model, expr):
    f = Face(base, model)
    E = model['eyes']; B = model.get('rest', {})
    m = model
    if expr == 'neutral':
        f.mouth(m.get('neutral_mouth', 'line'))
    elif expr == 'happy':
        for b in E:
            f.eye_closed(b, '^')
        f.mouth(m.get('happy_mouth', 'shout'))
        f.blush()
    elif expr == 'smug':
        for b in E:
            f.lid(b, 0.45)
        f.mouth('smirk')
    elif expr == 'angry':
        for b in E:
            f.lid(b, 0.30)
        f.brow(0, 4, -2); f.brow(1, 4, -2)
        f.mouth('grit')
    elif expr == 'crying':
        f.eye_closed(E[0], '>'); f.eye_closed(E[1], '<')
        f.brow(0, -3, 2, 2); f.brow(1, -3, 2, 2)
        f.tears()
        f.mouth('wail')
    elif expr == 'shocked':
        for b in E:
            f.pupils_small(b)
        f.brow(0, 0, 0, 4); f.brow(1, 0, 0, 4)
        f.mouth('o')
    elif expr == 'deadpan':
        for b in E:
            f.lid(b, 0.55)
        f.mouth('flat')
    elif expr == 'panic':
        for b in E:
            f.eye_white_ring(b)
        f.brow(0, -3, 1, 4); f.brow(1, -3, 1, 4)
        f.gloom()
        f.mouth('wobble')
    elif expr == 'sad':
        for b in E:
            f.lid(b, 0.25)
        f.brow(0, -3, 2, 1); f.brow(1, -3, 2, 1)
        f.mouth('frown')
    elif expr == 'blush':
        f.blush(strong=True)
        f.mouth('wavy')
    if m.get('post'):
        m['post'](f, expr)
    return f.a
