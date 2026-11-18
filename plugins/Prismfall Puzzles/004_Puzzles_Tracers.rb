#===============================================================================
# Prismfall Puzzles - 004 beam and power tracers
#-------------------------------------------------------------------------------
# BEAMS  pfp_beam("Lamp 1") traces from the source event in the direction it faces.
#   The playfield is every square that holds a "Beam x,y" overlay event (the map
#   generator puts one on each square a beam may cross). Devices, by event name:
#     "Mirror ..."   one-hot state even = "/" , odd = "\"
#     "Prism ..."    splits: straight on plus both sides
#     "Filter c ..." recolours the beam: c = 1-4 (each colour also has its own pattern in the art)
#     "Block ..." / "Boulder ..."   stops it
#     "Receptor ..." takes it (and stops it)
#   Lit overlay squares get one-hot state = colour (1-4). Returns { receptor name => colour }.
# POWER  pfp_power(:board) floods power from a board's source through "Node x,y"
#   events whose ports (N=1 E=2 S=4 W=8) are rotated clockwise by their one-hot state.
#   Lights "Strip x,y" events (self A) and returns the names of the lit lamps.
#   Boards are registered with PrismfallPuzzles.board(:id, { :source => [x, y, mask],
#     :nodes => { [x, y] => mask }, :lamps => { "Lamp door" => [x, y] }, :bridges => { "Drone" => mask } })
#===============================================================================
module PrismfallPuzzles
  BOARDS = {}
  MIRROR_SLASH = { 8 => 6, 6 => 8, 2 => 4, 4 => 2 }    # "/"
  MIRROR_BACK  = { 8 => 4, 4 => 8, 2 => 6, 6 => 2 }    # "\"
  SIDES        = { 8 => [4, 6], 2 => [4, 6], 4 => [8, 2], 6 => [8, 2] }

  module_function

  def clear_beams
    events("Beam ").each { |e| SELF_CH.each { |ch| set_self_switch(e, ch, false) } }
  end

  def beam(source, colour = 1, clear = true)
    src = event(source)
    return {} if !src
    clear_beams if clear
    lit = {}
    seen = {}
    queue = [[src.x, src.y, src.direction, colour]]
    until queue.empty?
      x, y, d, c = queue.shift
      200.times do
        dx, dy = DIRS[d]
        x += dx
        y += dy
        break if !$game_map.valid?(x, y) || seen[[x, y, d, c]]
        seen[[x, y, d, c]] = true
        dev = $game_map.events.values.find { |e| e.at_coordinate?(x, y) && e.name =~ /^(Mirror|Prism|Filter|Block|Boulder|Receptor)/ }
        kind = dev ? dev.name[/^\w+/] : nil
        case kind
        when "Receptor"
          lit[dev.name] = c
          break
        when "Block", "Boulder"
          break
        when "Mirror"
          d = (state_of(dev) % 2 == 0) ? MIRROR_SLASH[d] : MIRROR_BACK[d]
          next
        when "Prism"
          SIDES[d].each { |s| queue.push([x, y, s, c]) }
          next
        when "Filter"
          c = (dev.name[/^Filter (\d)/, 1] || c).to_i
          next
        end
        cell = event_at(x, y, "Beam ")
        break if !cell
        SELF_CH.each_with_index { |ch, i| set_self_switch(cell, ch, i + 1 == c) }
      end
    end
    refresh
    return lit
  end

  def board(id, data = nil)
    BOARDS[id] = data if data
    return BOARDS[id]
  end

  def rot_mask(mask, k)
    k.times { mask = ((mask << 1) & 0x0f) | (mask >> 3) }
    return mask
  end

  PORT = { 8 => 1, 6 => 2, 2 => 4, 4 => 8 }

  def power(id)
    b = BOARDS[id]
    return [] if !b
    masks = {}
    b[:nodes].each do |(x, y), m|
      ev = event_at(x, y, "Node")
      masks[[x, y]] = rot_mask(m, ev ? state_of(ev) : 0)
    end
    (b[:bridges] || {}).each do |name, m|       # movable conductors (the Gym 4 drone): where they stand now
      ev = event(name)
      masks[[ev.x, ev.y]] = (masks[[ev.x, ev.y]] || 0) | m if ev
    end
    sx, sy, sm = b[:source]
    masks[[sx, sy]] = sm || 15
    live = { [sx, sy] => true }
    queue = [[sx, sy]]
    until queue.empty?
      x, y = queue.shift
      DIRS.each do |d, (dx, dy)|
        next if masks[[x, y]] & PORT[d] == 0
        n = [x + dx, y + dy]
        next if live[n] || !masks[n] || masks[n] & PORT[10 - d] == 0
        live[n] = true
        queue.push(n)
      end
    end
    events("Strip ").each { |e| set_self_switch(e, "A", live[[e.x, e.y]] ? true : false) }
    refresh
    return (b[:lamps] || {}).select { |_n, pos| live[pos] }.keys
  end
end

def pfp_beam(source, colour = 1); return PrismfallPuzzles.beam(source, colour); end
def pfp_power(board);             return PrismfallPuzzles.power(board);        end
