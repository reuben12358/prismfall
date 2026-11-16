"""Builders for RGSS1 RPG::* objects + a small event-command DSL compiler.
Ivar orders mirror files saved by RPG Maker XP (order is irrelevant to loading)."""
import numpy as np
import rmarshal as M
from rmarshal import RObject, Sym, Table, Tone

O = lambda cls, **iv: RObject(Sym(cls), dict(iv))


def audio(name='', volume=100, pitch=100):
    return O('RPG::AudioFile', volume=volume, name=name, pitch=pitch)


def move_cmd(code, params=None):
    return O('RPG::MoveCommand', parameters=list(params or []), code=code)


def move_route(cmds=None, repeat=True, skippable=False):
    lst = list(cmds or []) + [move_cmd(0)]
    return O('RPG::MoveRoute', list=lst, skippable=skippable, repeat=repeat)


def ev_cmd(code, indent=0, params=None):
    return O('RPG::EventCommand', parameters=list(params or []), indent=indent, code=code)


def condition(switch1=None, switch2=None, var=None, self_sw=None):
    return O('RPG::Event::Page::Condition',
             switch2_valid=switch2 is not None, self_switch_ch=self_sw or 'A',
             switch1_id=switch1 or 1, switch1_valid=switch1 is not None,
             variable_value=(var[1] if var else 0), self_switch_valid=self_sw is not None,
             variable_id=(var[0] if var else 1), variable_valid=var is not None,
             switch2_id=switch2 or 1)


def graphic(char='', direction=2, pattern=0, hue=0, tile_id=0, opacity=255, blend=0):
    return O('RPG::Event::Page::Graphic', opacity=opacity, character_name=char, pattern=pattern,
             tile_id=tile_id, direction=direction, blend_type=blend, character_hue=hue)


TRIGGERS = {'action': 0, 'touch': 1, 'event_touch': 2, 'autorun': 3, 'parallel': 4}
MOVES = {'fixed': 0, 'random': 1, 'toward': 2, 'custom': 3}
DIRS = {'down': 2, 'left': 4, 'right': 6, 'up': 8, 'retain': 0, None: 2}


def page(cond=None, gfx=None, trigger=0, move_type=0, speed=3, freq=3, route=None, walk_anime=True,
         step_anime=False, dir_fix=False, through=False, on_top=False, cmds=None):
    lst = list(cmds or [])
    if not lst or lst[-1].code != 0 or lst[-1].indent != 0:
        lst.append(ev_cmd(0))
    return O('RPG::Event::Page', move_type=move_type, list=lst, condition=cond or condition(),
             direction_fix=dir_fix, move_route=route or move_route(), trigger=trigger,
             step_anime=step_anime, move_frequency=freq, graphic=gfx or graphic(),
             always_on_top=on_top, walk_anime=walk_anime, move_speed=speed, through=through)


def event(eid, name, x, y, pages):
    return O('RPG::Event', pages=pages, name=name, y=y, x=x, id=eid)


def rmap(tileset_id, width, height, data, events, bgm='', bgs='', autoplay_bgm=None, encounter_step=30,
         bgm_volume=100):
    return O('RPG::Map', bgm=audio(bgm, bgm_volume), tileset_id=tileset_id, events=events, bgs=audio(bgs, 80),
             autoplay_bgm=bool(bgm) if autoplay_bgm is None else autoplay_bgm, data=data, autoplay_bgs=bool(bgs),
             height=height, encounter_step=encounter_step, width=width, encounter_list=[])


def mapinfo(name, parent_id=0, order=0, expanded=False, scroll_x=0, scroll_y=0):
    return O('RPG::MapInfo', scroll_x=scroll_x, name=name, expanded=expanded, order=order, scroll_y=scroll_y,
             parent_id=parent_id)


def table3(layers):
    """layers: numpy (3, H, W) -> Table(W, H, 3)"""
    z, h, w = layers.shape
    return Table(w, h, z, 3, layers.astype(np.int16).copy())


# --------------------------------------------------------------------------- move-route DSL
MOVE_CODES = {'down': 1, 'left': 2, 'right': 3, 'up': 4, 'random': 9, 'toward_player': 10, 'away_player': 11,
              'forward': 12, 'backward': 13, 'turn_down': 16, 'turn_left': 17, 'turn_right': 18, 'turn_up': 19,
              'turn_right90': 20, 'turn_left90': 21, 'turn_180': 22, 'face_player': 25, 'face_away': 26,
              'walk_anime_on': 31, 'walk_anime_off': 32, 'step_anime_on': 33, 'step_anime_off': 34,
              'dir_fix_on': 35, 'dir_fix_off': 36, 'through_on': 37, 'through_off': 38, 'on_top_on': 39,
              'on_top_off': 40}


def route_cmds(items):
    out = []
    for it in items:
        if isinstance(it, str):
            k, _, n = it.partition(' ')
            if k == 'wait':
                out.append(move_cmd(15, [int(n)]))
            elif k in MOVE_CODES:
                for _ in range(int(n) if n else 1):
                    out.append(move_cmd(MOVE_CODES[k]))
            else:
                raise ValueError('unknown move %r' % it)
        elif isinstance(it, dict):
            (k, v), = it.items()
            if k == 'se': out.append(move_cmd(44, [audio(v, 100)]))
            elif k == 'script': out.append(move_cmd(45, [v]))
            elif k == 'graphic': out.append(move_cmd(41, list(v)))
            elif k == 'jump': out.append(move_cmd(14, list(v)))
            elif k == 'speed': out.append(move_cmd(29, [v]))
            elif k == 'freq': out.append(move_cmd(30, [v]))
            elif k == 'wait': out.append(move_cmd(15, [v]))
            elif k == 'switch_on': out.append(move_cmd(27, [v]))
            elif k == 'switch_off': out.append(move_cmd(28, [v]))
            elif k == 'opacity': out.append(move_cmd(42, [v]))
            else: raise ValueError('unknown move %r' % it)
        else:
            out.append(it)  # already a MoveCommand
    return out


def push_move(lst, who, cmds, indent, wait=True, repeat=False, skippable=True):
    mr = move_route(cmds, repeat=repeat, skippable=skippable)
    lst.append(ev_cmd(209, indent, [who, mr]))
    for c in mr.list[:-1]:
        lst.append(ev_cmd(509, indent, [c]))
    if wait:
        lst.append(ev_cmd(210, indent))


# --------------------------------------------------------------------------- command DSL
FLAGMAP = None   # set by build.py: callable(value, kind) -> int


def _f(v, kind):
    return FLAGMAP(v, kind) if FLAGMAP else v


import re as _re


def subst(text):
    """@@NAME in scripts/conditions -> the switch/variable id from flags.yaml (variables first)."""
    def rep(m):
        try:
            return str(_f(m.group(1), 'variables'))
        except ValueError:
            return str(_f(m.group(1), 'switches'))
    return _re.sub(r'@@([A-Z][A-Z0-9_]*)', rep, text)


def compile_cmds(items, indent=0, ctx=None):
    """items: list of DSL commands -> list of EventCommand (without the final 0)."""
    out = []
    for it in items or []:
        if isinstance(it, str):
            it = {'text': it}
        if not isinstance(it, dict):
            raise ValueError('bad command %r' % (it,))
        if 'if' in it or 'if_switch' in it or 'if_self' in it or 'if_var' in it:
            if 'if' in it: params = [12, subst(it['if'])]
            elif 'if_switch' in it:
                sid, on = it['if_switch']; sid = _f(sid, 'switches'); params = [0, int(sid), 0 if on else 1]
            elif 'if_self' in it:
                ch, on = it['if_self']; params = [2, ch, 0 if on else 1]
            else:
                vid, val = it['if_var'][:2]; vid = _f(vid, 'variables'); op = it['if_var'][2] if len(it['if_var']) > 2 else 1  # 1 = >=
                params = [1, int(vid), 0, int(val), op]
            out.append(ev_cmd(111, indent, params))
            out += compile_cmds(it.get('then', []), indent + 1, ctx)
            out.append(ev_cmd(0, indent + 1))
            if 'else' in it:
                out.append(ev_cmd(411, indent))
                out += compile_cmds(it['else'], indent + 1, ctx)
                out.append(ev_cmd(0, indent + 1))
            out.append(ev_cmd(412, indent))
            continue
        if 'choices' in it:
            ch = list(it['choices'])
            cancel = it.get('cancel', len(ch))
            out.append(ev_cmd(102, indent, [ch, cancel]))
            br = it.get('branches', [[] for _ in ch])
            for i, c in enumerate(ch):
                out.append(ev_cmd(402, indent, [i, c]))
                out += compile_cmds(br[i] if i < len(br) else [], indent + 1, ctx)
                out.append(ev_cmd(0, indent + 1))
            out.append(ev_cmd(404, indent))
            continue
        (k, v), = it.items()
        if k == 'text':
            lines = [l.rstrip() for l in str(v).split('\n') if l.strip()]
            for i, l in enumerate(lines):
                out.append(ev_cmd(101 if i == 0 else 401, indent, [l]))
        elif k == 'script':
            lines = [l.rstrip() for l in subst(str(v)).rstrip().split('\n') if l.strip()]
            for i, l in enumerate(lines):
                out.append(ev_cmd(355 if i == 0 else 655, indent, [l]))
        elif k == 'comment':
            for i, l in enumerate(str(v).split('\n')):
                out.append(ev_cmd(108 if i == 0 else 408, indent, [l]))
        elif k == 'switch':
            sid, on = v; sid = _f(sid, 'switches'); out.append(ev_cmd(121, indent, [int(sid), int(sid), 0 if on else 1]))
        elif k == 'var':
            vid, val = v; vid = _f(vid, 'variables'); out.append(ev_cmd(122, indent, [int(vid), int(vid), 0, 0, int(val)]))
        elif k == 'story':   # advance the main-quest stage, never move it backwards
            vid = _f('STORY', 'variables')
            out.append(ev_cmd(355, indent, ['pbSet(%d, %d) if pbGet(%d) < %d' % (vid, int(v), vid, int(v))]))
        elif k == 'selfswitch':
            ch, on = v; out.append(ev_cmd(123, indent, [ch, 0 if on else 1]))
        elif k == 'transfer':
            d = DIRS.get(v.get('dir', 'retain'), v.get('dir', 0))
            out.append(ev_cmd(201, indent, [0, int(v['map']), int(v['x']), int(v['y']), d, 0 if v.get('fade') else 1]))
        elif k == 'se': out.append(ev_cmd(250, indent, [audio(v, 80)]))
        elif k == 'me': out.append(ev_cmd(249, indent, [audio(v, 100)]))
        elif k == 'bgm': out.append(ev_cmd(241, indent, [audio(v, 100)]))
        elif k == 'wait': out.append(ev_cmd(106, indent, [int(v)]))
        elif k == 'waitmove': out.append(ev_cmd(210, indent))
        elif k == 'exit': out.append(ev_cmd(115, indent))
        elif k == 'erase': out.append(ev_cmd(116, indent))
        elif k == 'heal': out.append(ev_cmd(314, indent, [0]))
        elif k == 'transparent': out.append(ev_cmd(208, indent, [int(v)]))
        elif k == 'tone': out.append(ev_cmd(223, indent, [Tone(*v[:4]), int(v[4])]))
        elif k == 'label': out.append(ev_cmd(118, indent, [v]))
        elif k == 'jump_label': out.append(ev_cmd(119, indent, [v]))
        elif k == 'common_event': out.append(ev_cmd(117, indent, [int(v)]))
        elif k == 'move':
            push_move(out, v.get('who', 0), route_cmds(v['route']), indent, v.get('wait', True),
                      v.get('repeat', False), v.get('skippable', True))
        elif k == 'raw':
            out.append(ev_cmd(v[0], indent, v[1]))
        else:
            raise ValueError('unknown command %r' % k)
    return out


# --------------------------------------------------------------------------- Essentials event patterns
def door_pages(char, pattern, direction, target):
    """Animated door, identical to what Essentials' compiler (update_door_event) produces."""
    tgt = ev_cmd(201, 0, [0, int(target['map']), int(target['x']), int(target['y']),
                          DIRS.get(target.get('dir', 'up'), 8), 1])
    l1 = []
    push_move(l1, 0, route_cmds([{'se': 'Door enter'}, 'wait 2', 'turn_left', 'wait 2', 'turn_right', 'wait 2',
                                 'turn_up', 'wait 2']), 0)
    push_move(l1, -1, route_cmds(['through_on', 'up', 'through_off']), 0)
    l1.append(ev_cmd(208, 0, [0]))
    l1.append(ev_cmd(355, 0, ['Followers.follow_into_door']))
    l1.append(ev_cmd(210, 0))
    push_move(l1, 0, route_cmds(['wait 2', 'turn_right', 'wait 2', 'turn_left', 'wait 2', 'turn_down', 'wait 2']), 0)
    l1.append(ev_cmd(223, 0, [Tone(-255, -255, -255, 0), 6]))
    l1.append(ev_cmd(106, 0, [8]))
    l1.append(ev_cmd(208, 0, [1]))
    l1.append(tgt)
    l1.append(ev_cmd(223, 0, [Tone(0, 0, 0, 0), 6]))
    l2 = [ev_cmd(111, 0, [12, 'get_self.onEvent?']), ev_cmd(208, 1, [0]),
          ev_cmd(355, 1, ['Followers.hide_followers'])]
    push_move(l2, 0, route_cmds(['turn_left', 'wait 6']), 1)
    l2.append(ev_cmd(208, 1, [1]))
    push_move(l2, -1, route_cmds(['down']), 1)
    l2.append(ev_cmd(355, 1, ['Followers.put_followers_on_player']))
    push_move(l2, 0, route_cmds(['turn_up', 'wait 2', 'turn_right', 'wait 2', 'turn_down', 'wait 2']), 1)
    l2 += [ev_cmd(0, 1), ev_cmd(412, 0), ev_cmd(355, 0, ['setTempSwitchOn("A")'])]
    g = lambda: graphic(char, direction, pattern)
    return [page(gfx=g(), trigger=1, cmds=l1),
            page(cond=condition(switch1=22), gfx=g(), trigger=3, cmds=l2)]


def warp_pages(target, se='Door exit', fade=False):
    cmds = []
    if se:
        cmds.append(ev_cmd(250, 0, [audio(se, 80)]))
    cmds.append(ev_cmd(201, 0, [0, int(target['map']), int(target['x']), int(target['y']),
                                DIRS.get(target.get('dir', 'retain'), 0), 0 if fade else 1]))
    return [page(trigger=1, cmds=cmds)]


def safeq(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def trainer_pages(char, ttype, tname, version=0, intro='...', lose='...', after='...', direction=2,
                  rules=None, cond=None):
    """Same structure as Essentials' convert_to_trainer_event (single battle, no rematch)."""
    combo = ':%s, "%s"' % (ttype, safeq(tname)) + (', %d' % version if version else '')
    l1 = compile_cmds([{'script': 'pbTrainerIntro(:%s)' % ttype}, {'script': 'pbNoticePlayer(get_self)'},
                       {'text': intro}] + [{'script': r} for r in (rules or [])])
    l1.append(ev_cmd(111, 0, [12, 'TrainerBattle.start(%s)' % combo]))
    l1.append(ev_cmd(123, 1, ['A', 0]))
    l1 += [ev_cmd(0, 1), ev_cmd(412, 0), ev_cmd(355, 0, ['pbTrainerEnd'])]
    g = lambda: graphic(char, direction)
    p2cond = condition(self_sw='A')
    if cond is not None:
        p2cond.ivars.update({k: v for k, v in cond.ivars.items() if k.startswith(('switch', 'variable'))})
    return [page(cond=cond, gfx=g(), trigger=2, cmds=l1),
            page(cond=p2cond, gfx=g(), trigger=0, cmds=compile_cmds([{'text': after}]))]


def item_pages(item, hidden=False):
    l1 = [ev_cmd(111, 0, [12, 'pbItemBall(:%s)' % item]), ev_cmd(123, 1, ['A', 0]), ev_cmd(0, 1),
          ev_cmd(411, 0), ev_cmd(0, 1), ev_cmd(412, 0)]
    return [page(gfx=graphic('' if hidden else 'Object ball'), cmds=l1),
            page(cond=condition(self_sw='A'))]
