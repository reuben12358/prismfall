#===============================================================================
# Prismfall Puzzles - 002 rooms: reset, tiered hints, skip, checkers
#-------------------------------------------------------------------------------
# A room is registered once (the generated Plugins/Prismfall Maps/007_PuzzleRooms.rb
# does it from mapgen/puzzles/, the same data the solver proves):
#
#   PrismfallPuzzles.room(:g1_hall, {
#     :name   => "Weaving Hall", :map => 131,
#     :start  => [12, 18, 8],                      # x, y, direction after a reset
#     :reset  => { :vars => { 305 => 0 }, :switches => { 305 => false },
#                  :states => { "T1" => 0 }, :forget => [:crates] },
#     :solved => { :vars => { 305 => 2 }, :at => [21, 2, 8] },   # what "Skip" applies
#     :hints  => ["nudge", "the key fact", "the walkthrough"]
#   })
#
# Events call:
#   pfp_apprentice(:g1_hall, "Pim")   the gym apprentice menu (Reset / Hint / Skip / Leave)
#   pfp_reset(:g1_hall)               in-world reset (dungeon levers, bells); pfp_reset(id, false) = no fade/move
#   pfp_hint(:g1_hall)                show the best hint earned so far
#   pfp_skip?                         `puzzleskip` password active
#   pfp_check(:id)  -> [:ok] | [:fail, :reason]
#   pfp_check!(:id) -> true/false, prints the registered line for the reason and counts the failure
#   pfp_fail(:room, "text")           print a failure line that says what went wrong, count it
#===============================================================================
module PrismfallPuzzles
  ROOMS    = {}
  CHECKERS = {}

  module_function

  def room(id, data = nil)
    ROOMS[id] = data if data
    return ROOMS[id]
  end

  def room_log(id)
    store[:rooms] ||= {}
    store[:rooms][id] ||= { :resets => 0, :fails => 0, :hints => 0, :skipped => false }
    return store[:rooms][id]
  end

  def skip?
    return true if $game_switches && $game_switches[SKIP_SWITCH]
    return defined?(Prismfall::Passwords) && Prismfall::Passwords.active?(:PUZZLE_SKIP) ? true : false
  end

  # Applies a { :vars, :switches, :states, :self, :forget, :proc } block on the room's map.
  def apply_state(r, block)
    return if !block
    (block[:vars] || {}).each { |k, v| $game_variables[k] = v }
    (block[:switches] || {}).each { |k, v| $game_switches[k] = v }
    map_id = r[:map] || $game_map.map_id
    if map_id == $game_map.map_id
      (block[:states] || {}).each { |n, k| set_state(n, k) }
      (block[:self] || {}).each do |n, chs|
        ev = event(n)
        chs.each { |ch, v| set_self_switch(ev, ch, v) } if ev
      end
    end
    (block[:forget] || []).each { |k| forget_positions(k, map_id) }
    block[:proc].call if block[:proc]
    refresh
  end

  # Moved events go back to their map squares, the player to the room's start tile.
  def home_events(names = nil)
    $game_map.events.each_value do |e|
      next if names && !names.any? { |n| e.name.start_with?(n) }
      ox, oy = e.instance_variable_get(:@event).x, e.instance_variable_get(:@event).y
      e.moveto(ox, oy) if e.x != ox || e.y != oy
    end
  end

  def place_player(pos)
    return if !pos
    $game_player.moveto(pos[0], pos[1])
    $game_player.direction = pos[2] if pos[2]
    $game_player.straighten
    $game_temp.followers.put_followers_on_player if $game_temp.respond_to?(:followers)
  end

  def reset(id, fade = true, count = true)
    r = ROOMS[id]
    return false if !r
    work = proc do
      apply_state(r, r[:reset])
      if r[:map].nil? || r[:map] == $game_map.map_id
        home_events(r[:home]) if r[:home] != false
        place_player(r[:start]) if fade
      end
      $game_map.refresh
    end
    if fade
      pbFadeOutIn { work.call }
    else
      work.call
    end
    room_log(id)[:resets] += 1 if count
    return true
  end

  def solve(id, fade = true)
    r = ROOMS[id]
    return false if !r || !r[:solved]
    work = proc do
      apply_state(r, r[:solved])
      place_player(r[:solved][:at]) if r[:solved][:at] && (r[:map].nil? || r[:map] == $game_map.map_id)
      $game_map.refresh
    end
    if fade
      pbFadeOutIn { work.call }
    else
      work.call
    end
    room_log(id)[:skipped] = true
    return true
  end

  # Tier 1 is always available; each reset or failed check earns the next one.
  def hint_tier(id)
    r = ROOMS[id]
    return 0 if !r || !r[:hints] || r[:hints].empty?
    log = room_log(id)
    return [1 + log[:resets] + log[:fails], r[:hints].length].min
  end

  def hint(id, speaker = nil)
    r = ROOMS[id]
    tier = hint_tier(id)
    return false if tier == 0
    log = room_log(id)
    log[:hints] = tier if tier > log[:hints]
    pre = speaker ? "#{speaker}: " : ""
    pbMessage(pre + _INTL(r[:hints][tier - 1]))
    if tier < r[:hints].length
      pbMessage(_INTL("(Hint {1} of {2}. Reset the room or get it wrong once more and there'll be a clearer one.)",
                      tier, r[:hints].length))
    end
    return true
  end

  def apprentice(id, name = "Apprentice", greeting = nil)
    r = ROOMS[id]
    if !r
      pbMessage(_INTL("{1}: Nothing to fix in here today.", name))
      return
    end
    pbMessage("#{name}: " + _INTL(greeting || "Tangled? I can put the room back, or give you a nudge."))
    loop do
      cmds = [_INTL("Reset the room"), _INTL("Hint")]
      cmds.push(_INTL("Skip this room")) if skip? && r[:solved]
      cmds.push(_INTL("Leave it"))
      c = pbMessage(_INTL("What'll it be?"), cmds, cmds.length)
      case cmds[c]
      when _INTL("Reset the room")
        reset(id)
        pbMessage("#{name}: " + _INTL(r[:reset_text] || "There. Just as it was when you walked in."))
        break
      when _INTL("Hint")
        hint(id, name)
      when _INTL("Skip this room")
        if pbConfirmMessage(_INTL("Have {1} solve this room for you?", name))
          solve(id)
          pbMessage("#{name}: " + _INTL(r[:skip_text] || "Done. Nobody has to know."))
          break
        end
      else
        break
      end
    end
  end

  #-----------------------------------------------------------------------------
  # Checkers: a block returning [:ok] or [:fail, :reason]; lines say what went wrong.
  #-----------------------------------------------------------------------------
  def checker(id, room_id = nil, lines = {}, &block)
    CHECKERS[id] = { :room => room_id, :lines => lines, :proc => block }
  end

  def check(id)
    c = CHECKERS[id]
    return [:fail, :no_checker] if !c
    ret = c[:proc].call
    ret = (ret ? [:ok] : [:fail, :wrong]) if !ret.is_a?(Array)
    return ret
  end

  def check!(id)
    c = CHECKERS[id]
    ret = check(id)
    return true if ret[0] == :ok
    line = c && c[:lines][ret[1]]
    fail!(c && c[:room], line || "That isn't right yet.")
    return false
  end

  def fail!(room_id, text)
    room_log(room_id)[:fails] += 1 if room_id
    pbMessage(_INTL(text)) if text
    return false
  end
end

def pfp_apprentice(id, name = "Apprentice", greeting = nil); PrismfallPuzzles.apprentice(id, name, greeting); end
def pfp_reset(id, fade = true);  return PrismfallPuzzles.reset(id, fade);  end
def pfp_solve(id, fade = true);  return PrismfallPuzzles.solve(id, fade);  end
def pfp_hint(id, speaker = nil); return PrismfallPuzzles.hint(id, speaker); end
def pfp_skip?;                   return PrismfallPuzzles.skip?;            end
def pfp_check(id);               return PrismfallPuzzles.check(id);        end
def pfp_check!(id);              return PrismfallPuzzles.check!(id);       end
def pfp_fail(room_id, text);     return PrismfallPuzzles.fail!(room_id, text); end
