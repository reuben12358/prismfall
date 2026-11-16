"""Lossless JSON encoding of rmarshal object trees (for templates/stamps we store in mapgen/data)."""
import base64
import numpy as np
import rmarshal as M


def to_j(o):
    if o is None or isinstance(o, (bool, int, float)):
        return o
    if isinstance(o, M.Sym):
        return {'$sym': str(o)}
    if isinstance(o, M.RBytes):
        return {'$bytes': base64.b64encode(bytes(o)).decode()}
    if isinstance(o, str):
        return o
    if isinstance(o, list):
        return [to_j(x) for x in o]
    if isinstance(o, dict):
        return {'$hash': [[to_j(k), to_j(v)] for k, v in o.items()]}
    if isinstance(o, M.RObject):
        return {'$o': o.cls, 'iv': {k: to_j(v) for k, v in o.ivars.items()}}
    if isinstance(o, M.Table):
        return {'$table': [o.xsize, o.ysize, o.zsize, o.dim], 'data': o.data.reshape(-1).tolist()}
    if isinstance(o, M.Tone):
        return {'$tone': o.v}
    if isinstance(o, M.Color):
        return {'$color': o.v}
    if isinstance(o, M.RUserDef):
        return {'$udef': o.cls, 'data': base64.b64encode(o.data).decode()}
    raise TypeError(type(o))


def from_j(j):
    if j is None or isinstance(j, (bool, int, float, str)):
        return j
    if isinstance(j, list):
        return [from_j(x) for x in j]
    if '$sym' in j:
        return M.Sym(j['$sym'])
    if '$bytes' in j:
        return M.RBytes(base64.b64decode(j['$bytes']))
    if '$hash' in j:
        return {from_j(k): from_j(v) for k, v in j['$hash']}
    if '$o' in j:
        return M.RObject(M.Sym(j['$o']), {k: from_j(v) for k, v in j['iv'].items()})
    if '$table' in j:
        x, y, z, dim = j['$table']
        return M.Table(x, y, z, dim, np.array(j['data'], dtype=np.int16).reshape((z, y, x)))
    if '$tone' in j:
        return M.Tone(*j['$tone'])
    if '$color' in j:
        return M.Color(*j['$color'])
    if '$udef' in j:
        return M.RUserDef(M.Sym(j['$udef']), base64.b64decode(j['data']))
    raise ValueError(j)
