#===============================================================================
# Prismfall Puzzles - 005 step hooks, clocks, pursuers
#-------------------------------------------------------------------------------
#   PrismfallPuzzles.step_hook(map_id, :key) { |from, to| ... }   runs after each player step on that map only
#       from / to = [x, y] of the step just taken (pfp_step_hook is the same call)
#   pfp_metronome(var, frames, beats)   call every frame from a parallel event: V = (V + 1) % beats each `frames`
#   pfp_step_clock(var, period)         step-driven clock: V = (V + 1) % period; returns true when it wraps
#   pfp_pursue(name, mode)              one pursuer move per call; returns true when it has caught the player
#       :chase   one square toward the player (longer axis first, then the other; never through walls)
#       :mirror  repeats the player's last step mirrored left-right
#       :echo    repeats the player's steps `delay` steps late (PrismfallPuzzles.echo_delay[name], default 4)
#       :creep   :chase, but only while the player faces away from it (Thistledown's armchairs)
#===============================================================================
module PrismfallPuzzles
  STEP_HOOKS = {}

  module_function

  def step_hook(map_id, key = :main, &block)
    STEP_HOOKS[map_id] ||= {}
    STEP_HOOKS[map_id][key] = block
  end

  def last_step
    return @last_step || [[0, 0], [0, 0]]
  end

  def run_step_hooks
    return if !$game_map || !$game_player
    to = [$game_player.x, $game_player.y]
    from = (@prev_pos && @prev_map == $game_map.map_id) ? @prev_pos : to
    @prev_pos = to
    @prev_map = $game_map.map_id
    return if from == to
    @last_step = [from, to]
    trail = (store[:trail] ||= [])
    trail.push([to[0] - from[0], to[1] - from[1]])
    trail.shift while trail.length > 32
    hooks = STEP_HOOKS[$game_map.map_id]
    hooks&.each_value { |blk| blk.call(from, to) }
  end

  def reset_trail
    store[:trail] = []
    @prev_pos = nil
  end

  def metronome(var, frames, beats)
    return false if Graphics.frame_count % frames != 0
    cycle(var, beats)
    return true
  end

  def step_clock(var, period)
    return cycle(var, period) == 0
  end

  def echo_delay
    return (@echo_delay ||= Hash.new(4))
  end

  def try_shift(ev, dir)
    return false if !dir || !can_shift?(ev, dir)
    ev.direction = dir
    shift(ev, dir)
    return true
  end

  def facing_away?(ev)
    pl = $game_player
    dx, dy = ev.x - pl.x, ev.y - pl.y
    fx, fy = DIRS[pl.direction]
    return (dx * fx) + (dy * fy) < 0       # strictly in the half-plane behind the player
  end

  def pursue(name, mode = :chase)
    ev = event(name)
    return false if !ev
    pl = $game_player
    case mode
    when :chase, :creep
      if mode == :chase || facing_away?(ev)
        dx, dy = pl.x - ev.x, pl.y - ev.y
        horiz = (dx > 0) ? 6 : ((dx < 0) ? 4 : nil)
        vert  = (dy > 0) ? 2 : ((dy < 0) ? 8 : nil)
        order = (dx.abs >= dy.abs) ? [horiz, vert] : [vert, horiz]
        if dx.abs + dy.abs > 1
          order.compact.each { |d| break if try_shift(ev, d) }
        end
      end
    when :mirror
      from, to = last_step
      sx, sy = to[0] - from[0], to[1] - from[1]
      d = DIRS.key([-sx, sy])
      try_shift(ev, d)
    when :echo
      trail = store[:trail] || []
      step = trail[-1 - echo_delay[name]]
      try_shift(ev, DIRS.key(step)) if step
    end
    return (ev.x - pl.x).abs + (ev.y - pl.y).abs <= ((mode == :mirror) ? 0 : 1)
  end
end

def pfp_step_hook(map_id, key = :main, &block); PrismfallPuzzles.step_hook(map_id, key, &block); end
def pfp_metronome(var, frames, beats);  return PrismfallPuzzles.metronome(var, frames, beats); end
def pfp_step_clock(var, period);        return PrismfallPuzzles.step_clock(var, period);       end
def pfp_pursue(name, mode = :chase);    return PrismfallPuzzles.pursue(name, mode);            end

EventHandlers.add(:on_player_step_taken, :prismfall_puzzles_steps,
  proc { PrismfallPuzzles.run_step_hooks }
)
EventHandlers.add(:on_enter_map, :prismfall_puzzles_trail,
  proc { |_old_map_id| PrismfallPuzzles.reset_trail if $PokemonGlobal }
)
