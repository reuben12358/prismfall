import re, json, collections
secs = collections.OrderedDict(); cur = None; mon = None; comment_before = []
for line in open('/home/claude/fangame/pbs/trainers.txt', encoding='utf-8'):
    raw = line.rstrip('\n')
    if raw.startswith('#'):
        comment_before.append(raw[1:].strip()); continue
    m = re.match(r'^\[([A-Z0-9_]+),([^,\]]+)(?:,(\d+))?\]', raw)
    if m:
        key = (m.group(1), m.group(2), int(m.group(3) or 0))
        cur = {'type': key[0], 'name': key[1], 'ver': key[2], 'items': '', 'mons': [], 'comment': [c for c in comment_before if c and not set(c) <= set('-=')][-3:]}
        secs['%s|%s|%d' % key] = cur; mon = None; comment_before = []; continue
    if cur is None: continue
    s = raw.strip()
    if s.startswith('Items ='): cur['items'] = s.split('=', 1)[1].strip()
    elif s.startswith('Pokemon ='):
        sp, lv = [x.strip() for x in s.split('=', 1)[1].split(',')[:2]]
        mon = {'sp': sp, 'lv': int(lv)}; cur['mons'].append(mon)
    elif '=' in s and mon is not None:
        k, v = [x.strip() for x in s.split('=', 1)]
        mon[k] = v
    elif '=' in s:
        k, v = [x.strip() for x in s.split('=', 1)]; cur[k] = v
json.dump(secs, open('/tmp/wt/trainers.json', 'w'), indent=0)
if __name__ == '__main__':
    import sys
    pat = sys.argv[1] if len(sys.argv) > 1 else 'LEADER_|RIVAL_|HOLLOW_|MERIDIAN_|CHAMPION'
    for k, v in secs.items():
        if re.match(pat, v['type']):
            print(k, '|', ' / '.join('%s %d%s' % (mm['sp'], mm['lv'], ('@'+mm['Item']) if 'Item' in mm else '') for mm in v['mons']), '||', ' '.join(v['comment'])[:120])
