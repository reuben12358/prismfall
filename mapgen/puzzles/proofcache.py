"""proofcache: remember a slow proof's result while its inputs are unchanged (the step-level Gym 8 search and the
Gym 9 Glasshouse take minutes; build.py runs every proof on every build).  The key is the proof's name plus an md5 of
its module's source and the built maps it reads; any change to either re-runs the proof.  One file for every proof:
mapgen/puzzles/proof_cache.json (only the latest key per proof is kept)."""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'maps_out', 'Data')
PATH = os.path.join(HERE, 'proof_cache.json')


def cached(name, module_file, mids, fn):
    h = hashlib.md5(open(module_file, 'rb').read())
    for mid in mids:
        p = os.path.join(OUT, 'Map%03d.rxdata' % mid)
        h.update(open(p, 'rb').read() if os.path.exists(p) else b'-')
    key = h.hexdigest()
    try:
        data = json.load(open(PATH))
    except (OSError, ValueError):
        data = {}
    hit = data.get(name)
    if hit and hit.get('key') == key:
        return hit['ok'], hit['lines'] + ['  (cached: the module and maps %s are unchanged since this was proved)' % ','.join(map(str, mids))]
    ok, lines = fn()
    try:
        data = json.load(open(PATH))
    except (OSError, ValueError):
        data = {}
    data[name] = {'key': key, 'ok': ok, 'lines': lines}
    with open(PATH, 'w') as f:
        json.dump(data, f, indent=1, sort_keys=True)
    return ok, lines
