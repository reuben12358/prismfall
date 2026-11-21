import re, json, collections
def parse(path):
    data = collections.OrderedDict(); cur = None; typ = None
    for line in open(path, encoding='utf-8'):
        s = line.split('#')[0].rstrip() if not line.lstrip().startswith('[') else line.rstrip()
        if not s.strip(): continue
        m = re.match(r'\[(\d+)(?:,(\d+))?\]\s*(?:#\s*(.*))?', s.strip())
        if m:
            mid, ver, nm = int(m.group(1)), int(m.group(2) or 0), (m.group(3) or '').strip()
            cur = data.setdefault((mid, ver), {'name': nm, 'types': collections.OrderedDict()}); typ = None; continue
        t = s.strip()
        if re.match(r'^[A-Za-z]+(,\d+)?$', t):
            typ = t.split(',')[0]; cur['types'].setdefault(typ, []); continue
        mm = re.match(r'^(\d+),(\w+),(\d+)(?:,(\d+))?$', t)
        if mm and typ:
            cur['types'][typ].append((int(mm.group(1)), mm.group(2), int(mm.group(3)), int(mm.group(4) or mm.group(3))))
    return data
base = parse('/home/claude/fangame/pbs/encounters.txt')
tiers = parse('/home/claude/fangame/pbs/encounters_badgetiers.txt')
out = {'base': {'%d,%d' % k: v for k, v in base.items()}, 'tiers': {'%d,%d' % k: v for k, v in tiers.items()}}
json.dump(out, open('/tmp/wt/enc.json', 'w'), indent=0)
if __name__ == '__main__':
    import sys
    vers = collections.defaultdict(list)
    for (mid, ver), v in base.items(): vers[mid].append((ver, v['name'], list(v['types'].keys())))
    for mid in sorted(vers): print(mid, vers[mid][0][1], [(a, c) for a, b, c in vers[mid]])
    print('tiers maps:', sorted(set(k[0] for k in tiers)))
