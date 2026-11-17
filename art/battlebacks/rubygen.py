"""Tiny Python -> Ruby literal writer for the Bridge's generated art profiles."""


class Sym(str):
    """A Ruby Symbol."""


def S(name):
    return Sym(name)


def rb(v, ind=0):
    pad = "  " * ind
    if isinstance(v, Sym):
        return ":" + str(v)
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "nil"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        s = repr(round(v, 9))
        return s
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(v, (list, tuple)):
        if all(not isinstance(x, (dict, list, tuple)) for x in v):
            return "[" + ", ".join(rb(x) for x in v) + "]"
        return "[\n" + ",\n".join(pad + "  " + rb(x, ind + 1) for x in v) + "\n" + pad + "]"
    if isinstance(v, dict):
        items = []
        for k, x in v.items():
            ks = (":" + str(k)) if isinstance(k, Sym) else rb(k)
            items.append("%s => %s" % (ks, rb(x, ind + 1)))
        one = "{ " + ", ".join(items) + " }"
        if len(one) < 150 and "\n" not in one:
            return one
        return "{\n" + ",\n".join(pad + "  " + it for it in items) + "\n" + pad + "}"
    raise TypeError(type(v))
