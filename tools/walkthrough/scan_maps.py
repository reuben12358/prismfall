import sys, os, re, json, glob
sys.path.insert(0, '/home/claude/fangame/mapgen')
import rmarshal as M
out = {}
pat_item = re.compile(r'(pbItemBall|pbReceiveItem|pbGetItem|HiddenItem|pbAddPokemon|pbAddPokemonSilent|WildBattle\.start|TrainerBattle\.start|pbTrainerBattle|gym_battle|rival_battle|boss|pf_trial|setBattleRule|pbPokemonMart|PokemonMart|Prismfall\.\w+)')
for p in sorted(glob.glob('/home/claude/fangame/maps_out/Data/Map[0-9]*.rxdata')):
    mid = int(re.search(r'Map(\d+)', p).group(1))
    m = M.load_file(p)
    evs = m.ivars.get('events', {})
    rec = []
    for eid, ev in evs.items():
        name = ev.ivars.get('name', '')
        x, y = ev.ivars.get('x'), ev.ivars.get('y')
        scripts = []
        for pg in ev.ivars.get('pages', []):
            for cmd in pg.ivars.get('list', []):
                code = cmd.ivars.get('code'); params = cmd.ivars.get('parameters', [])
                if code in (355, 655) and params:
                    s = params[0]
                    if isinstance(s, str) and pat_item.search(s):
                        scripts.append(s.strip())
                elif code == 126 and params:  # change items
                    scripts.append('CHANGE_ITEM %r' % (params,))
                elif code == 111 and params and len(params) > 1 and isinstance(params[-1], str) and pat_item.search(str(params[-1])):
                    scripts.append('IF ' + str(params[-1]))
        if scripts or 'Item' in str(name):
            rec.append({'id': eid, 'name': str(name), 'at': [x, y], 'scripts': scripts})
    out[mid] = rec
json.dump(out, open('/tmp/wt/map_events.json', 'w'), indent=1, default=str)
print(len(out))
