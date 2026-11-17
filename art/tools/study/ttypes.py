"""List trainer types (id, title, sprite) from a fangame's ttypes.dat via the safe pure-Python marshal reader.
python3 -I ttypes.py PATH"""
import sys, os
sys.path.insert(0, '/home/claude/fangame/mapgen')
import rmarshal as rm

d = rm.load_file(sys.argv[1])
items = d.items() if isinstance(d, dict) else enumerate(d)
for k, v in items:
    if v is None:
        continue
    iv = v.ivars if hasattr(v, 'ivars') else (v if isinstance(v, dict) else {})
    def g(*names):
        for n in names:
            for kk in (n, '@' + n, rm.Sym(n)):
                if kk in iv:
                    return iv[kk]
        return ''
    fl = g('flags') or {}
    tid = ''
    if isinstance(fl, dict):
        for kk, vv in fl.items():
            if str(kk) == 'ID':
                tid = vv
    print('%s|%s|%s|%s' % (tid, k, g('title'), g('sprite')))
