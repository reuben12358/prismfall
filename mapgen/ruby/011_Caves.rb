#===============================================================================
# Prismfall Maps - 011 cave mechanics (map builder 13; mapgen/ruby/011_Caves.rb, copied by build.py)
#-------------------------------------------------------------------------------
# pfm_cart_ride(paths, off)   Brinecut Mine 1F (DUNGEON_PUZZLES D4 "points and brine"): ride the depot cart where
#                             the points send it.  S516 / S517 / S518 = points P1 / P2 / P3 (OFF = the left line).
#                             P1 left -> A (the dead-end drift); P1 right, P2 left -> D (the buffer: BUMP, back to the
#                             depot); P2 right, P3 left -> B (the ladder to B1F); P3 right -> C (the Thistledown mouth).
#                             paths = {"A" => "UUUL...", ...} (one letter per step from the depot), off = the step
#                             off the cart at each end.  V516 = where the cart stands (0 depot, 1 A, 2 B, 3 C);
#                             S519 = the cart is parked at B (it holds B1F's pump lever down).
# pfm_light_lamp(:key)        light a miner's lamp on a dark map: the darkness circle widens with every lamp lit
# pfm_cave_light              re-apply the lamps' light (the map's parallel event calls it; Flash still wins)
# pfm_tide_tick               Gullcry Caves (D6 "the tide counts your steps"): one step of the tide clock.  V526 =
#                             steps since the tide turned, S526 = high tide; every TIDE_PERIOD steps it turns.  Gulls
#                             cry in the last three steps.  When the sea comes in on a sand bar (an event named
#                             "Tide x,y" under you) the surge carries you to the nearest dry ground.
# pfm_gulls                   the gull roost: tells how near the turn is
#===============================================================================
module PrismfallCaves
  module_function

  def ev(name)
    return $game_map.events.values.find { |e| e.name == name }
  end

  def wait_moves(*chars)
    loop do
      Graphics.update
      Input.update
      pbUpdateSceneMap
      break if chars.compact.none? { |c| c.move_route_forcing || c.moving? }
    end
  end

  STEP = { "U" => PBMoveRoute::UP, "D" => PBMoveRoute::DOWN, "L" => PBMoveRoute::LEFT, "R" => PBMoveRoute::RIGHT }
  BACK = { "U" => "D", "D" => "U", "L" => "R", "R" => "L" }

  def route(path, speed = 5)
    return [PBMoveRoute::CHANGE_SPEED, speed] + path.chars.map { |c| STEP[c] }
  end
end

def pfm_cart_ride(paths, off)
  s = $game_switches
  key = !s[516] ? "A" : (!s[517] ? "D" : (!s[518] ? "B" : "C"))
  ride  = PrismfallCaves.ev("Ride cart")
  depot = PrismfallCaves.ev("Depot cart")
  return false if !ride || !depot
  pl = $game_player
  home = [pl.x, pl.y, pl.direction]
  pbSet(516, 0)
  s[519] = false
  $game_map.need_refresh = true
  pbSEPlay("Door exit", 80) rescue nil
  pbMoveRoute(depot, [PBMoveRoute::OPACITY, 0])
  ride.moveto(depot.x, depot.y)
  ride.direction = 8
  pl.moveto(depot.x, depot.y)
  pbMoveRoute(pl, [PBMoveRoute::OPACITY, 0])
  PrismfallCaves.wait_moves(pl)
  path = paths[key] || ""
  pbMoveRoute(ride, PrismfallCaves.route(path))
  pbMoveRoute(pl, PrismfallCaves.route(path))
  PrismfallCaves.wait_moves(pl, ride)
  if key == "D"
    pbSEPlay("Anim/Crash", 100) rescue nil
    $game_screen.start_shake(4, 8, 12) rescue nil
    pbMessage(_INTL("BUMP! The cart hits the buffer stop at the edge of the Cut, and rolls you all the way back."))
    back = path.reverse.chars.map { |c| PrismfallCaves::BACK[c] }.join
    pbMoveRoute(ride, PrismfallCaves.route(back, 4))
    pbMoveRoute(pl, PrismfallCaves.route(back, 4))
    PrismfallCaves.wait_moves(pl, ride)
    ride.moveto(0, 0)
    pl.moveto(home[0], home[1])
    pl.direction = home[2]
    pbMoveRoute(pl, [PBMoveRoute::OPACITY, 255])
  else
    ride.moveto(0, 0)
    pbSet(516, { "A" => 1, "B" => 2, "C" => 3 }[key])
    s[519] = (key == "B")
    $game_map.need_refresh = true
    pbMoveRoute(pl, [PBMoveRoute::OPACITY, 255] + PrismfallCaves.route(off[key] || "", 4))
    PrismfallCaves.wait_moves(pl)
  end
  pbMoveRoute(depot, [PBMoveRoute::OPACITY, 255])
  return true
end

def pfm_light_lamp(key)
  return false if pfm?(key)
  pfm_set(key)
  pfm_add(:"cave_lamps_#{$game_map.map_id}")
  pbSEPlay("Anim/Fire1", 70) rescue nil
  pfm_cave_light
  return true
end

def pfm_cave_light
  ds = $game_temp.darkness_sprite
  return if !ds || ds.disposed? || $PokemonGlobal.flashUsed
  n = pfm_count(:"cave_lamps_#{$game_map.map_id}")
  r = [ds.radiusMin + (26 * n), ds.radiusMax].min
  ds.radius = r if ds.radius != r
end

TIDE_PERIOD = 24

def pfm_tide_tick
  v = pbGet(526) + 1
  turned = false
  if v >= TIDE_PERIOD
    v = 0
    $game_switches[526] = !$game_switches[526]
    turned = true
  end
  pbSet(526, v)
  left = TIDE_PERIOD - v
  if !turned && left <= 3
    pbSEPlay("Cries/WINGULL", 60, 110 + (3 - left) * 10) rescue nil
  end
  return if !turned
  $game_map.need_refresh = true
  if $game_switches[526]
    pbSEPlay("Anim/Water1", 90) rescue nil
    pfm_tide_surge
  else
    pbSEPlay("Anim/Water2", 70) rescue nil
  end
end

def pfm_tide_bar?(x, y)
  return $game_map.events.values.any? { |e| e.x == x && e.y == y && e.name.start_with?("Tide ") }
end

def pfm_tide_surge
  pl = $game_player
  return if !pfm_tide_bar?(pl.x, pl.y)
  seen = { [pl.x, pl.y] => true }
  queue = [[pl.x, pl.y]]
  dest = nil
  until queue.empty? || dest
    x, y = queue.shift
    [[0, 1], [0, -1], [1, 0], [-1, 0]].each do |dx, dy|
      nx, ny = x + dx, y + dy
      next if seen[[nx, ny]] || !$game_map.valid?(nx, ny)
      seen[[nx, ny]] = true
      if pfm_tide_bar?(nx, ny)
        queue.push([nx, ny])
      elsif $game_map.passable?(nx, ny, 0)
        dest = [nx, ny]
        break
      end
    end
  end
  return if !dest
  pbMessage(_INTL("The sea comes in over the bar! The surge picks you up and drops you, soaked, on the rocks."))
  pbFadeOutIn do
    pl.moveto(dest[0], dest[1])
    $game_map.refresh
  end
end

def pfm_gulls
  left = TIDE_PERIOD - pbGet(526)
  pbMessage(_INTL("You clap your hands. The roost explodes into wings: a hundred gulls wheel over the pools and settle again."))
  if left <= 6
    pbMessage(_INTL("They won't settle. They keep lifting and looking seaward. The tide's about to turn."))
  elsif left <= 12
    pbMessage(_INTL("They settle, but they're restless. The turn isn't far off."))
  else
    pbMessage(_INTL("They settle quickly and tuck their heads in. The tide has only just turned: there's time."))
  end
  pbMessage(_INTL($game_switches[526] ? "The sea is in. The bars are under water." : "The sea is out. The sand bars are dry."))
end
