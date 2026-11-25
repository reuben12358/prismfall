#===============================================================================
# Prismfall Maps - 013 pf_echo_follow: the recorded-path follower (mapgen/ruby/013_EchoFollow.rb, copied by build.py)
#-------------------------------------------------------------------------------
# One mechanic, built once and used twice (story/34_SCRIPT_CH15.md):
#   * War 2, the War Convoy (926 Glass Dunes / 925 Steamline): "The sledges follow the PC's footprints exactly.
#     Step off the line and the sledge behind stops and creaks."
#   * Gym 14, the Requiem Crypt (393; design/GYM_PUZZLES.md "the echo"): ring the hand-bell to start recording, each
#     step is stored, up to 12; ring again and Morwen's echo appears at the start square and walks your recorded
#     steps, then stays (and holds plates). Ringing again erases her. V370 G14_ECHO_LEN = steps recorded.
#
# CONVOY (live): each follower event stands where the player stood (its place in line x spacing) steps ago.
#   pf_echo_follow(:convoy, "Sledge", spacing: 1, lane_tag: 7)
#       followers = every event whose name starts with "Sledge" (sorted by name), or an Array of event names/ids.
#       The line starts at the player's tile. Optional lane (the marked road): lane_tag: a terrain tag id,
#       lane: [[x, y], ...] tiles, or lane: :key for a block registered with PrismfallMaps::EchoFollow.lane(:key).
#       Off the lane the step isn't recorded, the first sledge creaks (SE + "!") and the convoy waits until the
#       player is back on the last recorded tile (or on a lane tile next to it).
#   pf_echo_follow(:stop)         the convoy ends; the events stay where they are
#   pf_echo_follow(:off?)         has the player left the line?        pf_echo_follow(:active?)
#   pf_echo_follow(:arrived?, x1, y1, x2, y2)    every follower inside that rectangle (the trench-head handover)
#   pf_echo_follow(:lead_at?, x, y)              the first follower stands on that tile
#
# REPLAY (the crypt echo):
#   pf_echo_follow(:record, max: 12, var: 370)   start recording from the player's tile (keep: :last = a sliding
#                                                window of the last `max` steps instead of the first)
#   pf_echo_follow(:recording?)
#   pf_echo_follow(:replay, "Morwen's echo", self_switch: "A")
#       stops recording; the event appears on the start square (its self switch is set, if given), walks the
#       recorded steps through anything (she's an echo) and stays. Returns the number of steps walked.
#   pf_echo_follow(:clear, "Morwen's echo", self_switch: "A")    erases her and the recording
#   pf_echo_follow(:echo_at?, "Morwen's echo", x, y)             does she hold that plate?
#   pf_echo_follow(:length)                                      steps recorded so far
#
# Everything is saved (PrismfallMaps.flags[:echo], in $PokemonGlobal): after a load or a battle the followers and
# the echo are put back where the record says they stood.
#===============================================================================
module PrismfallMaps
  module EchoFollow
    DIRS       = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }
    CREAK_SE   = "Strength push"
    MAX_RECORD = 12
    LANES      = {}

    module_function

    # A named lane test: PrismfallMaps::EchoFollow.lane(:steamline) { |x, y| ... true on the road ... }
    def lane(key, &block)
      LANES[key] = block
    end

    def store
      return (PrismfallMaps.flags[:echo] ||= {})
    end

    def convoy; return store[:convoy]; end
    def record; return store[:record]; end

    def event(ref)
      return nil if !$game_map
      return ref if !ref.is_a?(Integer) && !ref.is_a?(String) && !ref.is_a?(Symbol)
      return $game_map.events[ref] if ref.is_a?(Integer)
      return $game_map.events.values.find { |e| e.name == ref.to_s }
    end

    def events_for(spec)
      return [] if !$game_map
      if spec.is_a?(Array)
        return spec.map { |s| event(s) }.compact
      end
      return $game_map.events.values.select { |e| e.name.start_with?(spec.to_s) }.sort_by { |e| [e.name, e.id] }
    end

    def dir_for(dx, dy)
      return DIRS.key([dx, dy])
    end

    # One animated step in dir (through whatever is there), or a jump when the tiles aren't neighbours.
    def step_to(ev, x, y)
      return false if ev.x == x && ev.y == y
      dir = dir_for(x - ev.x, y - ev.y)
      if !dir
        ev.moveto(x, y)
        return true
      end
      was = ev.through
      ev.through = true
      ev.move_speed = $game_player.move_speed if $game_player && ev.respond_to?(:move_speed=)
      case dir
      when 2 then ev.move_down(false)
      when 4 then ev.move_left(false)
      when 6 then ev.move_right(false)
      when 8 then ev.move_up(false)
      end
      ev.direction = dir if ev.respond_to?(:direction=)
      ev.through = was
      ev.moveto(x, y) if ev.x != x || ev.y != y   # the move was refused (direction fix, a locked event): never desync
      return true
    end

    def remember_moved(ev)
      $PokemonMap.addMovedEvent(ev.id) if $PokemonMap && $PokemonMap.respond_to?(:addMovedEvent)
    rescue StandardError
      nil
    end

    #---------------------------------------------------------------------------
    # Convoy
    #---------------------------------------------------------------------------
    def start_convoy(followers, spacing: 1, lane_tag: nil, lane: nil)
      evs = events_for(followers)
      return false if evs.empty? || !$game_player
      store[:convoy] = {
        :map     => $game_map.map_id,
        :ids     => evs.map { |e| e.id },
        :spacing => [spacing.to_i, 1].max,
        :trail   => [[$game_player.x, $game_player.y]],
        :off     => false,
        :lane_tag => lane_tag,
        :lane    => lane
      }
      return true
    end

    def stop_convoy
      c = store.delete(:convoy)
      return false if !c
      c[:ids].each { |id| ev = event(id); remember_moved(ev) if ev }
      return true
    end

    def on_lane?(c, x, y)
      if c[:lane_tag]
        tag = ($game_map.respond_to?(:terrain_tag)) ? $game_map.terrain_tag(x, y) : nil
        id = (tag.respond_to?(:id_number)) ? tag.id_number : tag
        return false if id != c[:lane_tag]
      end
      lane = c[:lane]
      return true if lane.nil?
      return lane.include?([x, y]) if lane.is_a?(Array)
      blk = LANES[lane]
      return (blk) ? (blk.call(x, y) ? true : false) : true
    end

    def creak(c)
      ev = event(c[:ids].first)
      pbSEPlay(CREAK_SE) rescue nil
      return if !ev || !$scene || !$scene.respond_to?(:spriteset)
      $scene.spriteset.addUserAnimation(Settings::EXCLAMATION_ANIMATION_ID, ev.x, ev.y, true, 3) rescue nil
    end

    # Where follower k (0 = first in line) should stand for this trail, or nil while the line is still too short.
    def place_for(c, k)
      i = c[:trail].length - 1 - ((k + 1) * c[:spacing])
      return (i >= 0) ? c[:trail][i] : nil
    end

    def advance_convoy(c)
      c[:ids].each_with_index do |id, k|
        ev = event(id)
        pos = place_for(c, k)
        next if !ev || !pos
        step_to(ev, pos[0], pos[1])
      end
      keep = (c[:ids].length * c[:spacing]) + 2
      c[:trail].shift while c[:trail].length > keep
    end

    def convoy_step(c, to)
      last = c[:trail].last
      return if to == last && !c[:off]
      if c[:off]
        near = (to[0] - last[0]).abs + (to[1] - last[1]).abs
        if to == last
          c[:off] = false          # back on the last footprint: the line picks up from here
          return
        elsif near == 1 && on_lane?(c, to[0], to[1])
          c[:off] = false          # rejoined the road beside it
        else
          return
        end
      elsif !on_lane?(c, to[0], to[1])
        c[:off] = true
        creak(c)
        return
      end
      c[:trail].push(to)
      advance_convoy(c)
    end

    def restore_convoy(c)
      c[:ids].each_with_index do |id, k|
        ev = event(id)
        pos = place_for(c, k)
        ev.moveto(pos[0], pos[1]) if ev && pos
      end
    end

    def followers
      c = convoy
      return [] if !c || c[:map] != $game_map.map_id
      return c[:ids].map { |id| event(id) }.compact
    end

    def arrived?(x1, y1, x2, y2)
      evs = followers
      return false if evs.empty?
      xs = [x1, x2].minmax
      ys = [y1, y2].minmax
      return evs.all? { |e| e.x.between?(xs[0], xs[1]) && e.y.between?(ys[0], ys[1]) }
    end

    def lead_at?(x, y)
      ev = followers.first
      return (ev && ev.x == x && ev.y == y) ? true : false
    end

    #---------------------------------------------------------------------------
    # Record and replay
    #---------------------------------------------------------------------------
    def start_record(max: MAX_RECORD, var: nil, keep: :first)
      return false if !$game_player
      store[:record] = { :map => $game_map.map_id, :start => [$game_player.x, $game_player.y], :steps => [],
                         :max => [max.to_i, 1].max, :var => var, :keep => keep, :on => true }
      $game_variables[var] = 0 if var && $game_variables
      @prev = store[:record][:start].dup
      @prev_map = $game_map.map_id
      return true
    end

    def record_step(r, from, to)
      d = [to[0] - from[0], to[1] - from[1]]
      return if !DIRS.value?(d)           # a jump or a warp inside the room isn't a step she can walk
      if r[:steps].length >= r[:max]
        return if r[:keep] != :last
        first = r[:steps].shift
        r[:start] = [r[:start][0] + first[0], r[:start][1] + first[1]]
      end
      r[:steps].push(d)
      $game_variables[r[:var]] = r[:steps].length if r[:var] && $game_variables
    end

    def length
      r = record
      return (r) ? r[:steps].length : 0
    end

    def wait_move(ev)
      120.times do
        break if !ev.respond_to?(:moving?) || !ev.moving?
        Graphics.update
        Input.update
        pbUpdateSceneMap if defined?(pbUpdateSceneMap)
      end
    end

    def set_self_switch(ev, ch, value)
      return if !ch || !$game_self_switches
      $game_self_switches[[$game_map.map_id, ev.id, ch]] = value
      $game_map.need_refresh = true if $game_map.respond_to?(:need_refresh=)
    end

    def replay(ref, self_switch: nil, wait: true)
      r = record
      ev = event(ref)
      return 0 if !r || !ev || r[:map] != $game_map.map_id
      r[:on] = false
      ev.moveto(r[:start][0], r[:start][1])
      set_self_switch(ev, self_switch, true)
      x, y = r[:start]
      r[:steps].each do |dx, dy|
        x += dx
        y += dy
        step_to(ev, x, y)
        wait_move(ev) if wait
      end
      r[:echo] = { :id => ev.id, :at => [x, y], :self_switch => self_switch }
      remember_moved(ev)
      return r[:steps].length
    end

    def clear(ref = nil, self_switch: nil)
      r = store.delete(:record)
      ev = event(ref) || (r && r[:echo] && event(r[:echo][:id]))
      ch = self_switch || (r && r[:echo] && r[:echo][:self_switch])
      set_self_switch(ev, ch, false) if ev
      $game_variables[r[:var]] = 0 if r && r[:var] && $game_variables
      return true
    end

    def echo_at?(ref, x, y)
      r = record
      ev = event(ref)
      return false if !r || !r[:echo] || !ev || r[:echo][:id] != ev.id
      return r[:echo][:at] == [x, y]
    end

    def restore_echo(r)
      e = r[:echo]
      return if !e
      ev = event(e[:id])
      return if !ev
      ev.moveto(e[:at][0], e[:at][1])
      set_self_switch(ev, e[:self_switch], true)
    end

    #---------------------------------------------------------------------------
    # Hooks
    #---------------------------------------------------------------------------
    def on_step
      return if !$game_map || !$game_player || !$PokemonGlobal
      to = [$game_player.x, $game_player.y]
      from = (@prev && @prev_map == $game_map.map_id) ? @prev : to
      @prev = to
      @prev_map = $game_map.map_id
      c = convoy
      convoy_step(c, to) if c && c[:map] == $game_map.map_id
      r = record
      record_step(r, from, to) if r && r[:on] && r[:map] == $game_map.map_id && from != to
    end

    def on_enter_map
      @prev = ($game_player) ? [$game_player.x, $game_player.y] : nil
      @prev_map = ($game_map) ? $game_map.map_id : nil
      return if !$game_map || !$PokemonGlobal
      c = convoy
      restore_convoy(c) if c && c[:map] == $game_map.map_id
      r = record
      if r && r[:map] == $game_map.map_id
        restore_echo(r)
      elsif r && r[:on]
        r[:on] = false                    # left the room mid-recording: the bell has to be rung again
      end
    end

    def call(mode, *args, **opts)
      case mode
      when :convoy     then return start_convoy(args[0], **opts)
      when :stop       then return stop_convoy
      when :active?    then return convoy ? true : false
      when :off?       then return (convoy && convoy[:off]) ? true : false
      when :arrived?   then return arrived?(*args)
      when :lead_at?   then return lead_at?(*args)
      when :record     then return start_record(**opts)
      when :recording? then return (record && record[:on]) ? true : false
      when :replay     then return replay(args[0], **opts)
      when :clear      then return clear(args[0], **opts)
      when :echo_at?   then return echo_at?(*args)
      when :length     then return length
      end
      raise ArgumentError, "pf_echo_follow: unknown mode #{mode.inspect}"
    end
  end
end

def pf_echo_follow(mode, *args, **opts)
  return PrismfallMaps::EchoFollow.call(mode, *args, **opts)
end

EventHandlers.add(:on_player_step_taken, :prismfall_echo_follow,
  proc { PrismfallMaps::EchoFollow.on_step }
)
EventHandlers.add(:on_enter_map, :prismfall_echo_follow,
  proc { |_old_map_id| PrismfallMaps::EchoFollow.on_enter_map }
)
