#===============================================================================
# Prismfall Puzzles - web trampolines (Gym 2, the Canopy, SPINE Revision 19).
#
# A taut web throws you JUMP tiles on, the way you stepped onto it; land on another taut web and it throws you again.
# A sticky web (or a ledge) stops you.  Land on nothing and Tamsin's safety net lowers you back to the room's start.
# The room's layout is registered from mapgen/puzzles/canopy.py (the same data the solver proves):
#   PrismfallPuzzles.web_room(map_id, { :jump => 3, :start => [x, y], :webs => { [x, y] => "w" | "s" | [var, taut] },
#                                       :floor => [[x, y], ...] })
#   [var, taut] = a Joltik web: taut when (var is 0) == taut ... i.e. zapping (var 0 <-> 1) flips its as-built state.
# Web events call pfp_web from a Player Touch page.
#===============================================================================
module PrismfallPuzzles
  @web_rooms = {}

  def self.web_room(map_id, data)
    data[:floor] = data[:floor].map { |c| [c[0], c[1]] }.to_h { |c| [c, true] } if data[:floor].is_a?(Array)
    @web_rooms[map_id] = data
  end

  def self.web_data; return @web_rooms[$game_map.map_id]; end

  # :taut, :sticky, :floor or nil (the drop)
  def self.web_kind(x, y)
    w = web_data or return nil
    k = w[:webs][[x, y]]
    if k.is_a?(Array)
      zapped = $game_variables[k[0]].to_i % 2 == 1
      return (k[1] ^ zapped) ? :taut : :sticky
    end
    return :taut if k == "w"
    return :sticky if k == "s"
    return :floor if w[:floor][[x, y]]
    return nil
  end

  def self.web_throw
    w = web_data or return
    pl = $game_player
    dx, dy = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }[pl.direction]
    jump = w[:jump] || 3
    20.times do
      pbSEPlay("Battle jump", 70, 120) rescue nil
      tx, ty = pl.x + dx * jump, pl.y + dy * jump
      ride(tx, ty)
      case web_kind(tx, ty)
      when :taut   then next                                   # thrown again, the same way
      when :sticky
        pbSEPlay("Anim/Sand", 60, 80) rescue nil
        return
      when :floor  then return
      end
      web_fall(w)                                              # nothing there: the safety net
      return
    end
  end

  def self.web_fall(w)
    pbSEPlay("Fall", 80) rescue (pbSEPlay("Battle damage weak") rescue nil)
    pbMessage(_INTL("...and nothing there to land on. You drop into Tamsin's safety net, far below."))
    pbFadeOutIn do
      $game_player.moveto(w[:start][0], w[:start][1])
      $game_player.turn_up
      $game_map.need_refresh = true
    end
    pbMessage(_INTL("The net lowers you, very gently, all the way back to the bottom of the hollow. A card is pinned to it: \"Sorry! -- T.L.\""))
    PrismfallPuzzles.fail!(w[:room], nil) rescue nil
  end
end

def pfp_web; PrismfallPuzzles.web_throw; end
