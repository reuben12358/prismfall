#===============================================================================
# Prismfall Puzzles - 003 movement mechanics
#-------------------------------------------------------------------------------
#   pfp_ride(x, y)                  jump the player along a line to (x, y) (spools, ropes, one-way silk)
#   pfp_turntable_ride(cx, cy)      the floor turns a quarter clockwise and the player rides: (dx, dy) -> (-dy, dx)
#   pfp_swap_map(map_id, fix = {})  fade to the same x,y on a twin map; fix = { [x, y] => [sx, sy] } landing fix-ups
#   pfp_push_line(dir, kind)        forced movement while the tile ahead holds a "<kind>..." event (Belt, Wind,
#                                   Current), or while the tile being left is ice; returns the steps taken
#   pfp_push(strength = false)      push the event that is running this script one tile (crates)
#   pfp_slide(name = nil)           push a block: it slides until something stops it; a "Hole ..." event swallows
#                                   it and becomes plugged (self A)
#   pfp_push_pair(a, b)             2-tile objects (pews): both halves move as one or not at all
#   pfp_follow(name) / pfp_unfollow(name)   puzzle followers (removed automatically on leaving the map)
#===============================================================================
module PrismfallPuzzles
  module_function

  def wait_while
    loop do
      Graphics.update
      Input.update
      pbUpdateSceneMap
      break if !yield
    end
  end

  def wait_frames(n)
    n.times { Graphics.update; Input.update; pbUpdateSceneMap }
  end

  def ride(x, y)
    pl = $game_player
    dx, dy = x - pl.x, y - pl.y
    return false if dx == 0 && dy == 0
    was = pl.through
    pl.through = true
    pl.jump(dx, dy)
    wait_while { pl.jumping? }
    pl.through = was
    pl.moveto(x, y) if pl.x != x || pl.y != y   # a jump that the engine refused still lands (deterministic)
    return true
  end

  CW = { 8 => 6, 6 => 2, 2 => 4, 4 => 8 }

  def turntable_ride(cx, cy, quarter_turns = 1)
    pl = $game_player
    quarter_turns.times do
      dx, dy = pl.x - cx, pl.y - cy
      pl.moveto(cx - dy, cy + dx)
      pl.direction = CW[pl.direction] || pl.direction
    end
    pl.straighten
    refresh
    return [pl.x, pl.y]
  end

  def swap_map(map_id, fix = {})
    x, y = $game_player.x, $game_player.y
    x, y = fix[[x, y]] if fix[[x, y]]
    dir = $game_player.direction
    pbFadeOutIn do
      $game_temp.player_new_map_id    = map_id
      $game_temp.player_new_x         = x
      $game_temp.player_new_y         = y
      $game_temp.player_new_direction = dir
      $scene.transfer_player(false)
      $game_map.autoplay
      $game_map.refresh
    end
    return true
  end

  def blocked_by_event?(x, y, ignore = [])
    $game_map.events.each_value do |e|
      next if ignore.include?(e) || e.through || !e.at_coordinate?(x, y)
      return true if e.character_name != "" || e.tile_id > 0
    end
    return false
  end

  def step_player(dir)
    pl = $game_player
    return false if !pl.can_move_in_direction?(dir)
    pl.direction = dir
    case dir
    when 2 then pl.move_down
    when 4 then pl.move_left
    when 6 then pl.move_right
    when 8 then pl.move_up
    end
    wait_while { pl.moving? }
    return true
  end

  # kind: an event-name prefix ("Belt", "Wind", "Current") or :ice
  def push_line(dir, kind, max = 64)
    pl = $game_player
    steps = 0
    while steps < max
      dx, dy = DIRS[dir]
      if kind == :ice
        break if !$game_map.terrain_tag(pl.x, pl.y).ice && steps > 0
      else
        break if !event_at(pl.x + dx, pl.y + dy, kind.to_s) && !(steps == 0 && event_at(pl.x, pl.y, kind.to_s))
      end
      break if !step_player(dir)
      steps += 1
    end
    return steps
  end

  def can_shift?(ev, dir, ignore = [])
    dx, dy = DIRS[dir]
    nx, ny = ev.x + dx, ev.y + dy
    return false if !$game_map.valid?(nx, ny)
    return false if $game_player.x == nx && $game_player.y == ny
    return false if !$game_map.passable?(ev.x, ev.y, dir, ev) || !$game_map.passable?(nx, ny, 10 - dir, ev)
    return false if blocked_by_event?(nx, ny, [ev] + ignore)
    return true
  end

  def shift(ev, dir)
    was = ev.through
    ev.through = true
    case dir
    when 2 then ev.move_down(false)
    when 4 then ev.move_left(false)
    when 6 then ev.move_right(false)
    when 8 then ev.move_up(false)
    end
    ev.through = was
  end

  def push(ev, strength = false)
    dir = $game_player.direction
    return false if !ev || !can_shift?(ev, dir)
    shift(ev, dir)
    pbSEPlay("Strength push") if strength
    wait_while { ev.moving? }
    $PokemonMap&.addMovedEvent(ev.id)
    return true
  end

  # Returns the squares travelled; yields each square reached (return :stop from the block to halt there).
  def slide(ev, dir = $game_player.direction, max = 64)
    return 0 if !ev
    n = 0
    while n < max && can_shift?(ev, dir)
      shift(ev, dir)
      wait_while { ev.moving? }
      n += 1
      hole = event_at(ev.x, ev.y, "Hole")
      if hole && !self_switch(hole, "A")
        set_self_switch(hole, "A", true)          # plugged
        set_self_switch(ev, "A", true)            # the block's own "gone" page
        pbSEPlay("Battle damage weak") rescue nil
        refresh
        break
      end
      break if block_given? && yield(ev.x, ev.y) == :stop
    end
    $PokemonMap&.addMovedEvent(ev.id) if n > 0
    return n
  end

  def push_pair(a, b)
    ea, eb = event(a), event(b)
    dir = $game_player.direction
    return false if !ea || !eb
    return false if !can_shift?(ea, dir, [eb]) || !can_shift?(eb, dir, [ea])
    shift(ea, dir)
    shift(eb, dir)
    wait_while { ea.moving? || eb.moving? }
    $PokemonMap&.addMovedEvent(ea.id)
    $PokemonMap&.addMovedEvent(eb.id)
    return true
  end

  #-----------------------------------------------------------------------------
  # Followers (v21.1 Followers API). Puzzle followers never leave their map.
  #-----------------------------------------------------------------------------
  def follow(name, common_event_id = nil)
    ev = event(name)
    return false if !ev
    store[:followers] ||= []
    Followers.add(ev.id, name, common_event_id)
    store[:followers].push(name) if !store[:followers].include?(name)
    return true
  end

  def unfollow(name)
    Followers.remove(name)
    (store[:followers] || []).delete(name)
    return true
  end

  def following?(name)
    return (store[:followers] || []).include?(name)
  end

  def drop_followers
    (store[:followers] || []).dup.each { |n| unfollow(n) }
  end
end

def pfp_ride(x, y);                    return PrismfallPuzzles.ride(x, y);                      end
def pfp_turntable_ride(cx, cy, n = 1); return PrismfallPuzzles.turntable_ride(cx, cy, n);       end
def pfp_swap_map(map_id, fix = {});    return PrismfallPuzzles.swap_map(map_id, fix);           end
def pfp_push_line(dir, kind);          return PrismfallPuzzles.push_line(dir, kind);            end
def pfp_push_pair(a, b);               return PrismfallPuzzles.push_pair(a, b);                 end
def pfp_follow(name, ce = nil);        return PrismfallPuzzles.follow(name, ce);                end
def pfp_unfollow(name);                return PrismfallPuzzles.unfollow(name);                  end
def pfp_following?(name);              return PrismfallPuzzles.following?(name);                end

class Interpreter
  def pfp_push(strength = false);  return PrismfallPuzzles.push(get_self, strength); end
  def pfp_slide(name = nil);       return PrismfallPuzzles.slide(name ? PrismfallPuzzles.event(name) : get_self); end
end

EventHandlers.add(:on_leave_map, :prismfall_puzzles_followers,
  proc { |_new_map_id, _new_map| PrismfallPuzzles.drop_followers if $PokemonGlobal }
)
