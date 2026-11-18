#===============================================================================
# Prismfall Puzzles - 001 core state helpers (design/GYM_PUZZLES.md section 3)
#-------------------------------------------------------------------------------
# Everything is deterministic and save-safe: puzzle state lives in Game
# Switches/Variables 301-600, in self switches, or in $PokemonGlobal.pf_puzzle
# (a saved Hash). All helpers find events by NAME on the current map.
#
#   pfp_ev(name) / pfp_evs(prefix)        event(s) by name / name prefix
#   pfp_cycle(var, n, step = 1)           V = (V + step) % n
#   pfp_flip(sw)                          toggle a Game Switch
#   pfp_flip_self(names, ch = "A")        toggle a self switch of each named event
#   pfp_state(name, k) / pfp_state_of(n)  one-hot multi-state events (0 = none, 1-4 = self A-D)
#   pfp_rotate(name, n = 4)               next one-hot state
#   pfp_save(key, names) / pfp_load(key)  saved x, y, direction of named events (Coral pattern)
#   pfp_restore!                          re-apply every saved position of this map (automatic on map entry)
#   pfp_forget(key)                       drop saved positions (room reset)
#===============================================================================
class PokemonGlobalMetadata
  attr_writer :pf_puzzle

  def pf_puzzle
    @pf_puzzle = {} if !@pf_puzzle
    return @pf_puzzle
  end
end

module PrismfallPuzzles
  SKIP_SWITCH   = 301   # PUZZLE_SKIP: mirror of the `puzzleskip` password
  ASSIST_SWITCH = 302   # PUZZLE_ASSIST: reserved ("hints on")
  ID_RANGE      = (301..600)
  SELF_CH       = ["A", "B", "C", "D"]
  DIRS          = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }

  module_function

  def store
    return $PokemonGlobal.pf_puzzle
  end

  def refresh
    $game_map.need_refresh = true if $game_map
  end

  def event(name)
    return nil if !$game_map
    return name if name.is_a?(Game_Event)
    return $game_map.events[name] if name.is_a?(Integer)
    $game_map.events.each_value { |e| return e if e.name == name }
    return nil
  end

  def events(prefix)
    return [] if !$game_map
    return $game_map.events.values.select { |e| e.name.start_with?(prefix) }.sort_by { |e| e.id }
  end

  def event_at(x, y, prefix = nil)
    $game_map.events.each_value do |e|
      next if e.x != x || e.y != y
      next if prefix && !e.name.start_with?(prefix)
      return e
    end
    return nil
  end

  def self_switch(ev, ch)
    return $game_self_switches[[$game_map.map_id, ev.id, ch]]
  end

  def set_self_switch(ev, ch, value)
    $game_self_switches[[$game_map.map_id, ev.id, ch]] = value
  end

  def cycle(var, n, step = 1)
    $game_variables[var] = ($game_variables[var].to_i + step) % n
    refresh
    return $game_variables[var]
  end

  def flip(sw)
    $game_switches[sw] = !$game_switches[sw]
    refresh
    return $game_switches[sw]
  end

  def flip_self(names, ch = "A")
    Array(names).each do |n|
      ev = event(n)
      next if !ev
      set_self_switch(ev, ch, !self_switch(ev, ch))
    end
    refresh
  end

  def state_of(name)
    ev = event(name)
    return 0 if !ev
    SELF_CH.each_with_index { |ch, i| return i + 1 if self_switch(ev, ch) }
    return 0
  end

  def set_state(name, k)
    ev = event(name)
    return if !ev
    SELF_CH.each_with_index { |ch, i| set_self_switch(ev, ch, i + 1 == k) }
    refresh
  end

  def rotate(name, n = 4)
    k = (state_of(name) + 1) % n
    set_state(name, k)
    return k
  end

  #-----------------------------------------------------------------------------
  # Saved positions. store[:pos][map_id][key] = { name => [x, y, dir] }
  #-----------------------------------------------------------------------------
  def positions(map_id = $game_map.map_id)
    store[:pos] ||= {}
    store[:pos][map_id] ||= {}
    return store[:pos][map_id]
  end

  def save_positions(key, names)
    h = {}
    Array(names).each do |n|
      ev = event(n)
      h[ev.name] = [ev.x, ev.y, ev.direction] if ev
    end
    positions[key] = h
    return h
  end

  def load_positions(key)
    h = positions[key]
    return false if !h
    h.each do |n, (x, y, d)|
      ev = event(n)
      next if !ev
      ev.moveto(x, y)
      ev.direction = d if d && d > 0
    end
    return true
  end

  def forget_positions(key, map_id = $game_map.map_id)
    positions(map_id).delete(key)
  end

  def restore!
    return if !$game_map
    positions.each_key { |k| load_positions(k) }
    refresh
  end
end

def pfp_ev(name);                    return PrismfallPuzzles.event(name);              end
def pfp_evs(prefix);                 return PrismfallPuzzles.events(prefix);           end
def pfp_cycle(var, n, step = 1);     return PrismfallPuzzles.cycle(var, n, step);      end
def pfp_flip(sw);                    return PrismfallPuzzles.flip(sw);                 end
def pfp_flip_self(names, ch = "A");  return PrismfallPuzzles.flip_self(names, ch);     end
def pfp_state(name, k);              return PrismfallPuzzles.set_state(name, k);       end
def pfp_state_of(name);              return PrismfallPuzzles.state_of(name);           end
def pfp_rotate(name, n = 4);         return PrismfallPuzzles.rotate(name, n);          end
def pfp_save(key, names);            return PrismfallPuzzles.save_positions(key, names); end
def pfp_load(key);                   return PrismfallPuzzles.load_positions(key);      end
def pfp_forget(key);                 return PrismfallPuzzles.forget_positions(key);    end
def pfp_restore!;                    return PrismfallPuzzles.restore!;                 end

# Saved positions come back whenever a map is (re)entered: RMXP forgets moved events on leaving a map.
EventHandlers.add(:on_enter_map, :prismfall_puzzles_restore,
  proc { |_old_map_id| PrismfallPuzzles.restore! }
)
