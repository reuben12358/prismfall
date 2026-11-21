import re, json
rows = []
t = open('/home/claude/fangame/design/MEGA_EVOLUTION.md', encoding='utf-8').read()
sec = t.split('### 5.1', 1)[1].split('### 5.2', 1)[0]
for line in sec.splitlines():
    if not line.startswith('|') or line.startswith('| Badges') or line.startswith('|---'): continue
    c = [x.strip() for x in line.strip().strip('|').split('|')]
    b = re.sub(r'\*', '', c[0]); m = re.search(r'\((\d+)\)\s*$', c[3])
    rows.append({'kind': 'stone', 'badges': int(b), 'item': re.sub(r'\*|\(\+.*?\)', '', c[1]).strip(), 'mega': c[2], 'where': c[3], 'map': int(m.group(1)) if m else None, 'how': c[4]})
z = open('/home/claude/fangame/design/Z_MOVES.md', encoding='utf-8').read()
for line in z.splitlines():
    m = re.match(r'^\| \**(\d+)\** (?:\(post-game\) )?\| (.+?) \| (.+?) \| (.+?) \|$', line)
    if m and 'Z' in m.group(2):
        mm = re.search(r'\((\d+)\)\s*$', m.group(3))
        rows.append({'kind': 'crystal', 'badges': int(m.group(1)), 'item': m.group(2).strip('* '), 'where': m.group(3), 'map': int(mm.group(1)) if mm else None, 'how': m.group(4)})
json.dump(rows, open('/tmp/wt/stones.json', 'w'), indent=0)
print(len(rows), [ (r['item'], r['badges'], r['map']) for r in rows if r['kind']=='crystal'])
