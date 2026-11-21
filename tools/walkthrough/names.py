import re, json
def names(path, key='Name'):
    out = {}; cur = None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\[([A-Za-z0-9_]+)(?:,\d+)?\]', line)
        if m: cur = m.group(1); continue
        if cur and line.startswith(key + ' ='):
            out.setdefault(cur, line.split('=', 1)[1].strip())
    return out
R = '/home/claude/ref/ebdx/PBS/'
P = '/home/claude/fangame/pbs/'
n = {'species': names(R + 'pokemon.txt'), 'moves': names(R + 'moves.txt'), 'abilities': names(R + 'abilities.txt'), 'items': names(R + 'items.txt')}
for f in ['items_fields.txt', 'items_zpower.txt']: n['items'].update(names(P + f))
n['moves'].update(names(P + 'moves_zpower.txt'))
n['ttypes'] = names(R + 'trainer_types.txt'); n['ttypes'].update(names(P + 'trainer_types.txt'))
json.dump(n, open('/tmp/wt/names.json', 'w'))
print({k: len(v) for k, v in n.items()}, n['species'].get('NIDORANfE'), n['items'].get('TM42'), n['ttypes'].get('POKEMONRANGER_F'), n['ttypes'].get('HOLLOW_THISTLE'))
tm = names(R + 'items.txt', 'Move')
n['tm_moves'] = {k: n['moves'].get(v, v) for k, v in tm.items() if k.startswith('TM') or k.startswith('HM') or k.startswith('TR')}
import yaml
fd = yaml.safe_load(open('/home/claude/fangame/design/FIELD_DEFAULTS.yaml'))
n['fields'] = {str(k): v.get('field') for k, v in fd['maps'].items()}
n['fieldstage'] = {str(k): v.get('stage') for k, v in fd['maps'].items() if v.get('stage')}
n['fieldwild'] = {str(k): v.get('wild') for k, v in fd['maps'].items() if v.get('wild')}
json.dump(n, open('/tmp/wt/names.json', 'w'))
print(n['tm_moves'].get('TM42'), n['tm_moves'].get('HM01'), len(n['fields']), n['fields'].get('520'), n['fields'].get('160'), n['fieldwild'])
