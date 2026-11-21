import re, json
t = open('/home/claude/fangame/design/EVENT_POKEMON.md', encoding='utf-8').read()
rows = []
for line in t.splitlines():
    if re.match(r'^\| \d+ \|', line):
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        rows.append({'n': c[0], 'mon': c[1], 'kind': c[2], 'ch': c[3], 'badges': c[4], 'where': c[5], 'how': c[6], 'why': c[7], 'quest': c[8], 'status': c[9]})
json.dump(rows, open('/tmp/wt/eventmons.json', 'w'), indent=0)
print(len(rows))
