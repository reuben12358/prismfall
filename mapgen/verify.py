#!/usr/bin/env python3
"""Verification helpers.
  verify.py roundtrip <files...>   load -> dump -> load, deep-compare (and report byte-identical files)
  verify.py compare <ours.rxdata> <reference.rxdata>   structural comparison (classes + ivar sets, recursively)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rmarshal as M


def eq(a, b, path='', errs=None):
    errs = [] if errs is None else errs
    if len(errs) > 5: return errs
    if type(a) is not type(b) and not (isinstance(a, str) and isinstance(b, str)):
        errs.append('%s: type %s vs %s' % (path, type(a).__name__, type(b).__name__)); return errs
    if isinstance(a, M.RObject):
        if a.cls != b.cls or set(a.ivars) != set(b.ivars):
            errs.append('%s: %s %s vs %s %s' % (path, a.cls, sorted(a.ivars), b.cls, sorted(b.ivars))); return errs
        for k in a.ivars: eq(a.ivars[k], b.ivars[k], path + '.' + k, errs)
    elif isinstance(a, list):
        if len(a) != len(b): errs.append('%s: len %d vs %d' % (path, len(a), len(b))); return errs
        for i, (x, y) in enumerate(zip(a, b)): eq(x, y, '%s[%d]' % (path, i), errs)
    elif isinstance(a, dict):
        if list(a) != list(b): errs.append('%s: keys differ' % path); return errs
        for k in a: eq(a[k], b[k], '%s{%r}' % (path, k), errs)
    elif isinstance(a, M.Table):
        if (a.xsize, a.ysize, a.zsize) != (b.xsize, b.ysize, b.zsize) or not np.array_equal(a.data, b.data):
            errs.append(path + ': table differs')
    elif isinstance(a, M.Color):
        if a.v != b.v: errs.append(path + ': color differs')
    elif a != b:
        errs.append('%s: %r vs %r' % (path, a, b))
    return errs


def shape(o, depth=0, seen=None):
    """class -> set of ivar names, collected recursively."""
    seen = {} if seen is None else seen
    if isinstance(o, M.RObject):
        seen.setdefault(str(o.cls), set()).update(o.ivars)
        for v in o.ivars.values(): shape(v, depth + 1, seen)
    elif isinstance(o, list):
        for v in o: shape(v, depth + 1, seen)
    elif isinstance(o, dict):
        for v in o.values(): shape(v, depth + 1, seen)
    return seen


def main():
    a = sys.argv[1:]
    if a[0] == 'roundtrip':
        same = ok = 0
        for f in a[1:]:
            b = open(f, 'rb').read(); o = M.loads(b); b2 = M.dumps(o); o2 = M.loads(b2)
            errs = eq(o, o2)
            if errs: print('MISMATCH', f, errs[:3])
            else: ok += 1
            same += b == b2
        print('roundtrip ok: %d/%d (byte-identical: %d)' % (ok, len(a) - 1, same))
    elif a[0] == 'compare':
        s1, s2 = shape(M.load_file(a[1])), shape(M.load_file(a[2]))
        bad = 0
        for cls in sorted(set(s1) | set(s2)):
            if cls in s1 and cls in s2 and s1[cls] != s2[cls]:
                print('ivar mismatch', cls, 'ours-only', s1[cls] - s2[cls], 'ref-only', s2[cls] - s1[cls]); bad += 1
            elif cls not in s2:
                print('class not in reference:', cls)
        print('structure', 'OK' if not bad else 'MISMATCH', 'classes:', sorted(s1))


if __name__ == '__main__':
    main()
