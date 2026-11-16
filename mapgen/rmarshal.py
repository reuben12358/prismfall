"""Pure-Python Ruby Marshal 4.8 reader/writer for RGSS1 (RPG Maker XP) data.

Safe by construction: decoding never executes anything; unknown classes become
generic RObject / RUserDef containers.  Run tools that read untrusted files with
`python3 -I`.

Python representation
  nil/true/false/Integer  -> None/True/False/int
  Float                   -> float
  String                  -> str  (utf-8; undecodable bytes -> RBytes)
  Symbol                  -> Sym (str subclass)
  Array / Hash            -> list / dict   (Hash default stored in RHashDefault)
  Object ('o')            -> RObject(cls, ivars)     ivars keys WITHOUT '@'
  _dump ('u') Table       -> Table ; Color / Tone -> Color / Tone ; others RUserDef
"""
import struct
import numpy as np


class Sym(str):
    __slots__ = ()

    def __repr__(self):
        return ':' + str.__str__(self)


class RBytes(bytes):
    """A Ruby String that is not valid UTF-8 (kept as raw bytes)."""


class PStr(str):
    """A Ruby String that was stored WITHOUT an encoding ivar (RMXP / Ruby 1.8 style); written back the same way."""
    __slots__ = ()


class RObject:
    __slots__ = ('cls', 'ivars')

    def __init__(self, cls, ivars=None):
        self.cls = cls
        self.ivars = ivars if ivars is not None else {}

    def __getattr__(self, k):
        try:
            return self.ivars[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        if k in RObject.__slots__:
            object.__setattr__(self, k, v)
        else:
            self.ivars[k] = v

    def get(self, k, d=None):
        return self.ivars.get(k, d)

    def __repr__(self):
        return '#<%s %s>' % (self.cls, ' '.join('@%s=%r' % kv for kv in list(self.ivars.items())[:6]))


class RUserDef:
    def __init__(self, cls, data):
        self.cls, self.data = cls, data

    def __repr__(self):
        return '#<%s _dump %d bytes>' % (self.cls, len(self.data))


class Table:
    """RGSS Table. data is numpy int16 array shaped (zsize, ysize, xsize)."""

    def __init__(self, xsize, ysize=1, zsize=1, dim=None, data=None):
        self.dim = dim if dim is not None else (3 if zsize > 1 else (2 if ysize > 1 else 1))
        self.xsize, self.ysize, self.zsize = xsize, ysize, zsize
        if data is None:
            data = np.zeros((zsize, ysize, xsize), dtype=np.int16)
        self.data = data

    def __getitem__(self, idx):
        if not isinstance(idx, tuple):
            idx = (idx,)
        x = idx[0]; y = idx[1] if len(idx) > 1 else 0; z = idx[2] if len(idx) > 2 else 0
        return int(self.data[z, y, x])

    def __setitem__(self, idx, v):
        if not isinstance(idx, tuple):
            idx = (idx,)
        x = idx[0]; y = idx[1] if len(idx) > 1 else 0; z = idx[2] if len(idx) > 2 else 0
        self.data[z, y, x] = v

    @classmethod
    def load(cls, b):
        dim, xs, ys, zs, n = struct.unpack_from('<5i', b, 0)
        arr = np.frombuffer(b, dtype='<i2', count=n, offset=20).astype(np.int16)
        return cls(xs, ys, zs, dim, arr.reshape((zs, ys, xs)).copy())

    def dump(self):
        n = self.xsize * self.ysize * self.zsize
        return struct.pack('<5i', self.dim, self.xsize, self.ysize, self.zsize, n) + \
            self.data.astype('<i2').tobytes()

    def __repr__(self):
        return '#<Table %dx%dx%d>' % (self.xsize, self.ysize, self.zsize)


class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0, a=255.0):
        self.v = [float(r), float(g), float(b), float(a)]

    def dump(self):
        return struct.pack('<4d', *self.v)

    def __repr__(self):
        return '#<%s %s>' % (type(self).__name__, self.v)


class Tone(Color):
    def __init__(self, r=0.0, g=0.0, b=0.0, gray=0.0):
        self.v = [float(r), float(g), float(b), float(gray)]


class RHashDefault(dict):
    default = None


# ----------------------------------------------------------------------------- reader
class Reader:
    def __init__(self, data):
        self.b = data
        self.p = 0
        self.syms = []
        self.objs = []

    def byte(self):
        c = self.b[self.p]; self.p += 1
        return c

    def read(self, n):
        s = self.b[self.p:self.p + n]; self.p += n
        return s

    def long(self):
        c = self.byte()
        if c > 127:
            c -= 256
        if c == 0:
            return 0
        if 5 <= c <= 127:
            return c - 5
        if -128 <= c <= -5:
            return c + 5
        if c > 0:
            x = 0
            for i in range(c):
                x |= self.byte() << (8 * i)
            return x
        n = -c
        x = 0
        for i in range(n):
            x |= self.byte() << (8 * i)
        return x - (1 << (8 * n))

    def bytes_(self):
        return self.read(self.long())

    def symbol(self):
        t = chr(self.byte())
        if t == ':':
            s = Sym(self.bytes_().decode('utf-8', 'replace'))
            self.syms.append(s)
            return s
        if t == ';':
            return self.syms[self.long()]
        if t == 'I':  # symbol with encoding ivars (Ruby 1.9+)
            s = self.symbol()
            for _ in range(self.long()):
                self.symbol(); self.obj()
            return s
        raise ValueError('expected symbol, got %r at %d' % (t, self.p))

    def reg(self, o):
        self.objs.append(o)
        return o

    @staticmethod
    def mkstr(raw):
        try:
            return raw.decode('utf-8')
        except UnicodeDecodeError:
            return RBytes(raw)

    def obj(self):
        t = chr(self.byte())
        if t == '0': return None
        if t == 'T': return True
        if t == 'F': return False
        if t == 'i': return self.long()
        if t == ':': self.p -= 1; return self.symbol()
        if t == ';': self.p -= 1; return self.symbol()
        if t == '@': return self.objs[self.long()]
        if t == '"':
            v = self.mkstr(self.bytes_())
            return self.reg(PStr(v) if isinstance(v, str) else v)
        if t == 'f':
            s = self.bytes_().decode()
            v = {'nan': float('nan'), 'inf': float('inf'), '-inf': float('-inf')}.get(s)
            return self.reg(v if v is not None else float(s.split('\0')[0]))
        if t == 'l':
            sign = chr(self.byte()); n = self.long() * 2
            v = int.from_bytes(self.read(n), 'little')
            return self.reg(-v if sign == '-' else v)
        if t == '[':
            n = self.long(); a = self.reg([])
            for _ in range(n): a.append(self.obj())
            return a
        if t in '{}':
            n = self.long(); h = self.reg(RHashDefault() if t == '}' else {})
            for _ in range(n):
                k = self.obj(); h[k] = self.obj()
            if t == '}': h.default = self.obj()
            return h
        if t == 'I':
            idx = len(self.objs)
            o = self.obj()
            if isinstance(o, PStr):          # string carried an encoding ivar -> normal (UTF-8) string
                o = str(o)
                if idx < len(self.objs):
                    self.objs[idx] = o
            for _ in range(self.long()):
                self.symbol(); self.obj()   # encoding ivars (E / encoding) -> ignored
            return o
        if t == 'o':
            cls = self.symbol(); o = self.reg(RObject(cls))
            for _ in range(self.long()):
                k = self.symbol(); o.ivars[k[1:] if k.startswith('@') else k] = self.obj()
            return o
        if t == 'u':
            cls = self.symbol(); raw = self.bytes_()
            if cls == 'Table': o = Table.load(raw)
            elif cls == 'Color': o = Color(*struct.unpack('<4d', raw))
            elif cls == 'Tone': o = Tone(*struct.unpack('<4d', raw))
            else: o = RUserDef(cls, raw)
            return self.reg(o)
        if t == 'S':
            cls = self.symbol(); o = self.reg(RObject(cls))
            for _ in range(self.long()):
                k = self.symbol(); o.ivars[k] = self.obj()
            return o
        if t == 'U':
            cls = self.symbol(); o = self.reg(RObject(cls)); o.ivars['__marshal_load'] = self.obj()
            return o
        if t == 'e':
            self.symbol(); return self.obj()
        if t == 'C':
            self.symbol(); return self.obj()
        if t in 'cm':
            return self.reg(Sym(self.bytes_().decode()))
        if t == '/':
            s = self.bytes_(); self.byte(); return self.reg(self.mkstr(s))
        raise ValueError('unsupported marshal type %r at %d' % (t, self.p - 1))


def loads(data):
    if data[:2] != b'\x04\x08':
        raise ValueError('not Marshal 4.8')
    r = Reader(data)
    r.p = 2
    return r.obj()


def load_file(path):
    with open(path, 'rb') as f:
        return loads(f.read())


# ----------------------------------------------------------------------------- writer
class Writer:
    """Writes RGSS1-style Marshal: plain '"' strings (no encoding ivar, like RMXP),
    symbols deduplicated with ';' links. Objects are never shared (no '@' links)."""

    def __init__(self, string_mode='utf8'):
        self.out = bytearray(b'\x04\x08')
        self.syms = {}
        self.string_mode = string_mode   # 'utf8' (Ruby 1.9+ style, I-wrapped :E=>true) or 'plain' (RMXP 1.8)

    def string(self, b):
        if self.string_mode == 'plain':
            self.out.append(ord('"')); self.bytes_(b)
        else:
            self.out.append(ord('I')); self.out.append(ord('"')); self.bytes_(b)
            self.long(1); self.symbol('E'); self.out.append(ord('T'))

    def long(self, n):
        o = self.out
        if n == 0: o.append(0)
        elif 0 < n < 123: o.append(n + 5)
        elif -124 < n < 0: o.append((n - 5) & 0xff)
        else:
            buf = bytearray()
            x = n
            for i in range(1, 5):
                buf.append(x & 0xff); x >>= 8
                if (n >= 0 and x == 0) or (n < 0 and x == -1):
                    o.append(i if n >= 0 else (256 - i)); o.extend(buf); return
            raise ValueError('long out of range %d' % n)

    def bytes_(self, b):
        self.long(len(b)); self.out.extend(b)

    def symbol(self, s):
        s = str(s)
        if s in self.syms:
            self.out.append(ord(';')); self.long(self.syms[s])
        else:
            self.syms[s] = len(self.syms)
            self.out.append(ord(':')); self.bytes_(s.encode('utf-8'))

    def obj(self, v):
        o = self.out
        if v is None: o.append(ord('0'))
        elif v is True: o.append(ord('T'))
        elif v is False: o.append(ord('F'))
        elif isinstance(v, Sym): self.symbol(v)
        elif isinstance(v, int):
            if -(1 << 30) <= v < (1 << 30):
                o.append(ord('i')); self.long(v)
            else:
                o.append(ord('l')); o.append(ord('-' if v < 0 else '+'))
                a = abs(v); nb = (a.bit_length() + 15) // 16 * 2
                self.long(nb // 2); o.extend(a.to_bytes(nb, 'little'))
        elif isinstance(v, float):
            o.append(ord('f'))
            s = repr(v) if v != int(v) else str(int(v))
            self.bytes_(s.encode())
        elif isinstance(v, RBytes): o.append(ord('"')); self.bytes_(bytes(v))
        elif isinstance(v, PStr): o.append(ord('"')); self.bytes_(v.encode('utf-8'))
        elif isinstance(v, str): self.string(v.encode('utf-8'))
        elif isinstance(v, (list, tuple)):
            o.append(ord('[')); self.long(len(v))
            for x in v: self.obj(x)
        elif isinstance(v, dict):
            o.append(ord('{')); self.long(len(v))
            for k, x in v.items(): self.obj(k); self.obj(x)
        elif isinstance(v, RObject):
            o.append(ord('o')); self.symbol(v.cls); self.long(len(v.ivars))
            for k, x in v.ivars.items():
                self.symbol('@' + k); self.obj(x)
        elif isinstance(v, Table):
            o.append(ord('u')); self.symbol('Table'); self.bytes_(v.dump())
        elif isinstance(v, Tone):
            o.append(ord('u')); self.symbol('Tone'); self.bytes_(v.dump())
        elif isinstance(v, Color):
            o.append(ord('u')); self.symbol('Color'); self.bytes_(v.dump())
        elif isinstance(v, RUserDef):
            o.append(ord('u')); self.symbol(v.cls); self.bytes_(v.data)
        else:
            raise TypeError('cannot marshal %r' % type(v))


def dumps(v, string_mode='utf8'):
    w = Writer(string_mode); w.obj(v)
    return bytes(w.out)


def dump_file(v, path, string_mode='utf8'):
    with open(path, 'wb') as f:
        f.write(dumps(v, string_mode))
