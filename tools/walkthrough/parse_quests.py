import re, json
t = open('/home/claude/fangame/design/TRIALS_QUESTS.md', encoding='utf-8').read()
cat = t.split('## Part 1. Catalogue', 1)[1].split('## Part 2.', 1)[0]
trial = None; rows = []
for line in cat.splitlines():
    m = re.match(r'### (.+)', line)
    if m: trial = m.group(1).strip(); continue
    if line.startswith('| **'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        nm = re.match(r'\*\*(.+?)\*\*\s*`(\w+)`', cells[0])
        rows.append({'trial': trial, 'name': nm.group(1), 'id': nm.group(2), 'ch': cells[1], 'unlock': cells[2], 'giver': cells[3],
                     'rank': cells[4], 'what': cells[5], 'reward': cells[6], 'touches': cells[7], 'status': cells[8]})
json.dump(rows, open('/tmp/wt/quests.json', 'w'), indent=0)
print(len(rows))
import collections
c = collections.Counter(r['ch'] for r in rows); print(sorted(c.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 99))
