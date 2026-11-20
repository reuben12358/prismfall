#===============================================================================
# DEV-ONLY: puzzle sessions for the playtest bot (run_puzzles.sh; never ship).
# The bot walks into a gym through its town door and solves the puzzle rooms with
# ordinary input only: arrow keys along BFS paths, Use on levers/ropes, walking
# into spools.  Nothing sets a switch or variable for it.
#   PLAYBOT_SESSION=gym1       map 147's Playhouse door -> Lobby -> Auditorium (aisle, curtain rope) -> Dorian
#   PLAYBOT_SESSION=gym2       map 120's Loomhouse door -> Lobby -> the Canopy (web trampolines, sticky webs, two Joltik) -> Tamsin
#   PLAYBOT_SESSION=house0 / house7 / house21   Gym 1 with 0 / 7 / 21 Saltmere townsfolk met: the house and Dorian's opening stage
#   PLAYBOT_SESSION=lofts      the optional Upper Lofts (with Tamsin's badge): Canopy Lofts -> Granny's Knot
#   PLAYBOT_SESSION=backstage  the optional Playhouse Backstage (D9): old revolve + Fly Loft
# New step kinds: [:use_from, map, x, y, dir]  stand on (x, y), face dir, press Use
#                 [:ride, map, x, y, dir]      stand on (x, y), walk into the thing in dir until thrown elsewhere
#                 [:shot, map, "name"]         screenshot when the map is idle
#===============================================================================
module PlayBot
  PUZZLE_START = { "gym1" => [147, :door, 150], "gym2" => [120, :door, 130], "lofts" => [131, 19, 5], "backstage" => [154, 2, 11],
                   "house0" => [154, 12, 28], "d2" => [525, 24, 8], "d7" => [562, 36, 21], "house7" => [154, 12, 28], "house21" => [154, 12, 28],
                   "d1" => [522, 6, 36] }
  # Gym 1 (SPINE Rev 14): the Pell Playhouse. A walk-through: lobby, up the aisle past the actors, one curtain rope.
  GYM1_PLAN = [
    [:shot, 147, "g1_00_outside_the_playhouse"],
    [:door, 147, 150],                    # map 147's Playhouse door (found by its transfer, wherever the town puts it)
    [:shot, 150, "g1_01_lobby"],
    [:bump, 150, 12, 5],                  # the auditorium doors
    [:shot, 154, "g1_02_auditorium"],
    [:goto, 154, 12, 17], [:shot, 154, "g1_03_up_the_aisle"],
    [:goto, 154, 12, 11], [:shot, 154, "g1_04_on_the_apron_curtain_in"],
    [:use_from, 154, 20, 11, 6], [:shot, 154, "g1_05_curtain_out"],
    [:goto, 154, 12, 8],  [:shot, 154, "g1_06_before_dorian"],
    [:talk, 154, 12, 7],                  # Warden Dorian (the AI plays the battle)
    [:shot, 154, "g1_07_badge"],
    [:done]
  ]
  # SPINE Rev 19: the Saltmere audience. PLAYBOT_SESSION=house0 / house7 / house21 starts in the auditorium with that many
  # townsfolk met (the first N of PrismfallPuzzles::AUDIENCE_PEOPLE, then the lantern quest), the aisle actors already
  # beaten, and shows the house, then Dorian's fight starting at the stage the house sets.
  HOUSE_PLAN = [
    [:shot, 154, "hs_00_back_of_the_house"],
    [:goto, 154, 12, 21], [:shot, 154, "hs_01_the_stalls"],
    [:goto, 154, 12, 11], [:use_from, 154, 20, 11, 6],
    [:goto, 154, 12, 8], [:talk, 154, 12, 7],
    [:shot, 154, "hs_02_after_the_show"],
    [:done]
  ]
  # Dungeons laid over the map builder's maps (puzzles/dungeons.py EVENTS): D2 the Deepwood's lantern hollow, D7 the Frost Loom
  D2_PLAN = [
    [:shot, 525, "d2_00_the_lantern_hollow"],
    [:talk, 525, 25, 7], [:shot, 525, "d2_01_post_alpha"],
    [:ride, 525, 28, 8, 6], [:shot, 525, "d2_02_through_the_first_curtain"],
    [:talk, 525, 33, 9], [:shot, 525, "d2_03_post_beta"],
    [:ride, 525, 34, 7, 8], [:shot, 525, "d2_04_onto_the_island"],
    [:talk, 525, 31, 2], [:shot, 525, "d2_05_tm19"],
    [:done]
  ]
  D7_PLAN = [
    [:shot, 562, "d7_00_the_frost_loom"],
    [:talk, 562, 40, 19], [:shot, 562, "d7_01_left_thread"],
    [:talk, 562, 42, 19], [:shot, 562, "d7_02_right_thread"],
    [:goto, 562, 47, 15], [:shot, 562, "d7_03_through_the_curtains"],
    [:talk, 562, 44, 12], [:shot, 562, "d7_04_the_cache"],
    [:done]
  ]
  # Gym 2 (SPINE Rev 19): the Loomhouse lobby, then the Canopy: web trampolines, sticky webs, two Joltik.
  GYM2_PLAN = [
    [:shot, 120, "g2_00_outside_the_loomhouse"],
    [:door, 120, 130],                    # map 120's Loomhouse door
    [:shot, 130, "g2_01_lobby"],
    [:goto, 130, 15, 4],                  # the stair up into the tree
    [:shot, 131, "g2_02_canopy_floor"],
    [:goto, 131, 12, 29], [:shot, 131, "g2_03_first_web"],
    [:ride, 131, 12, 29, 8], [:shot, 131, "g2_04_thrown_to_ledge_one"],
    [:ride, 131, 18, 24, 8],              # a web throws you onto a web: up to ledge two (Lass Orla is waiting)
    [:shot, 131, "g2_05_web_onto_web"],
    [:ride, 131, 6, 17, 8], [:shot, 131, "g2_06_held_by_a_sticky_web"],
    [:ride, 131, 6, 13, 6], [:shot, 131, "g2_07_thrown_sideways"],
    [:goto, 131, 10, 11], [:shot, 131, "g2_08_ledge_three"],
    [:talk, 131, 16, 10], [:shot, 131, "g2_09_joltik_one"],
    [:ride, 131, 2, 10, 8], [:talk, 131, 1, 5], [:shot, 131, "g2_10_joltik_two"],
    [:ride, 131, 2, 6, 2],
    [:ride, 131, 12, 10, 8], [:shot, 131, "g2_11_up_onto_b"],
    [:ride, 131, 12, 6, 6], [:shot, 131, "g2_12_across_to_tamsin"],
    [:goto, 131, 16, 5],
    [:talk, 131, 17, 5],                  # Warden Tamsin, double battle (the AI plays it)
    [:shot, 131, "g2_13_badge"],
    [:done]
  ]
  # The optional Upper Lofts (after Tamsin's badge): spools + the brass Meridian wire, then Granny's Knot.
  LOFTS_PLAN = [
    [:goto, 131, 20, 4], [:goto, 131, 20, 3], [:goto, 131, 20, 2],   # the stair behind Tamsin (a touch event on the top step)
    [:shot, 132, "lf_06_lofts_start"],
    [:talk, 132, 1, 21],                  # alpha cord
    [:ride, 132, 3, 22, 6],               # spool s1 -> west deck
    [:shot, 132, "lf_07_lofts_west_deck"],
    [:talk, 132, 3, 11],                  # the brass Meridian wire: the bridge swings out
    [:shot, 132, "lf_08_lofts_brass_wire"],
    [:ride, 132, 5, 12, 6],               # spool s3 -> east deck
    [:talk, 132, 18, 13],                 # gamma cord
    [:ride, 132, 20, 14, 6],              # spool s4 -> south deck
    [:ride, 132, 13, 20, 6],              # spool s2 -> north deck
    [:shot, 132, "lf_09_lofts_north_deck_bridge"],
    [:goto, 132, 17, 5], [:shot, 132, "lf_10_lofts_on_the_bridge"],
    [:goto, 132, 22, 2],
    [:shot, 134, "lf_11_grannys_knot"],
    [:talk, 134, 7, 9], [:talk, 134, 10, 9], [:talk, 134, 11, 9],
    [:shot, 134, "lf_12_knot_solved"],
    [:talk, 134, 5, 10], [:shot, 134, "lf_13_chest"],
    [:done]
  ]
  # Playhouse Backstage (D9, optional after Gym 2): the old revolving stage + Fly Loft.
  BACKSTAGE_PLAN = [
    [:goto, 154, 2, 11], [:bump, 154, 2, 10],
    [:shot, 151, "bs_00_old_revolve"],
    [:use_from, 151, 2, 17, 2], [:shot, 151, "bs_01_shipwreck"],
    [:goto, 151, 4, 13],  [:shot, 151, "bs_02_across_the_gangplank"],
    [:use_from, 151, 6, 10, 6], [:shot, 151, "bs_03_forest"],
    [:goto, 151, 2, 4],
    [:shot, 152, "bs_04_loft"],
    [:talk, 152, 21, 6], [:shot, 152, "bs_05_rope2_right_rail"],
    [:talk, 152, 22, 6], [:shot, 152, "bs_06_rope3"],
    [:goto, 152, 22, 4],
    [:use_from, 151, 18, 5, 8], [:shot, 151, "bs_07_throne"],
    [:goto, 151, 14, 10], [:shot, 151, "bs_08_through_flat_b"],
    [:goto, 151, 12, 7],  [:shot, 151, "bs_09_rostrum"],
    [:goto, 151, 12, 3],  [:goto, 151, 12, 2],
    [:arrive, 154], [:shot, 154, "bs_10_back_in_the_auditorium"],
    [:done]
  ]
  # PLAYBOT_SESSION=d1: the Glassed Orchard chime rows, with one deliberate wrong note first (the failure line)
  D1_PLAN = [
    [:talk, 522, 19, 33], [:shot, 522, "d1_00_chime_post"],
    [:goto, 522, 23, 16], [:shot, 522, "d1_01_wrong_note_first"],
    [:goto, 522, 4, 16],  [:shot, 522, "d1_02_low"],
    [:goto, 522, 23, 16], [:shot, 522, "d1_03_middle"],
    [:goto, 522, 35, 25], [:shot, 522, "d1_04_high_hedge_shatters"],
    [:goto, 522, 38, 2],  [:shot, 522, "d1_05_past_the_hedge"],
    [:talk, 522, 38, 1],  [:shot, 522, "d1_06_satchel"],
    [:done]
  ]

  def self.find_door(rpg_events, target_map)
    rpg_events.each do |e|
      e.pages.each do |pg|
        pg.list.each { |c| return [e.x, e.y] if c.code == 201 && c.parameters[0] == 0 && c.parameters[1] == target_map }
      end
    end
    return nil
  end

  class << self
    alias puz_plan plan unless method_defined?(:puz_plan)
    def plan
      return GYM1_PLAN if SESSION == "gym1"
      return GYM2_PLAN if SESSION == "gym2"
      return LOFTS_PLAN if SESSION == "lofts"
      return BACKSTAGE_PLAN if SESSION == "backstage"
      return D1_PLAN if SESSION == "d1"
      return HOUSE_PLAN if SESSION.start_with?("house")
      return D2_PLAN if SESSION == "d2"
      return D7_PLAN if SESSION == "d7"
      return puz_plan
    end

    alias puz_drive_plan drive_plan unless method_defined?(:puz_drive_plan)
    def drive_plan
      step = plan[@step]
      return puz_drive_plan if !step || ![:use_from, :ride, :shot].include?(step[0])
      kind, map = step
      if @step_start == 0
        @step_start = @frame
        @step_frames = 0
        log("step #{@step}: #{step.inspect}  [vars 305-313: #{(305..313).map { |i| $game_variables[i] }.inspect} sw 305-312: #{(305..312).map { |i| $game_switches[i] ? 1 : 0 }.join}]")
      end
      @step_frames += 1
      return wait_for_map if $game_map.map_id != map
      return stuck("step timed out") if @step_frames > 3600
      case kind
      when :shot
        return if @idle < 24
        shot(step[2])
        next_step
      when :use_from
        x, y, d = step[2], step[3], step[4]
        return walk_to(x, y) if $game_player.x != x || $game_player.y != y
        return if @idle < 12
        if $game_player.direction != d
          @dir = d
        elsif @talk_at && @went_busy && @went_busy > @talk_at
          next_step
        elsif !@talk_at || @frame - @talk_at > 120
          @talk_at = @frame
          press(B::USE)
        end
      when :ride
        x, y, d = step[2], step[3], step[4]
        if @ride_from
          far = ($game_player.x - x).abs + ($game_player.y - y).abs > 1
          if far && !$game_player.jumping? && @idle >= 10
            @ride_from = nil
            next_step
          elsif !far
            @dir = d
          end
          return
        end
        return walk_to(x, y) if $game_player.x != x || $game_player.y != y
        return if @idle < 12
        @ride_from = [x, y]
        @dir = d
      end
    end
  end
end

module Game
  class << self
    alias puzbot_start_new start_new unless method_defined?(:puzbot_start_new)
    def start_new
      st = PlayBot::PUZZLE_START[PlayBot::SESSION]
      if st && st[1] == :door           # start one step below the town's door into the gym (towns get rebuilt)
        door = PlayBot.find_door(load_data(sprintf("Data/Map%03d.rxdata", st[0])).events.values, st[2])
        st = door ? [st[0], door[0], door[1] + 1] : nil
        PlayBot.log("no door to map #{PlayBot::PUZZLE_START[PlayBot::SESSION][2]} on map #{PlayBot::PUZZLE_START[PlayBot::SESSION][0]}") if !st
      end
      if st
        PrismfallMaps.define_singleton_method(:apply_start_position) do
          $data_system.start_map_id, $data_system.start_x, $data_system.start_y = *st
          true
        end
      end
      puzbot_start_new
      return if !st
      PlayBot.plan.map! do |step|                # [:door, map, target] -> [:bump, map, door x, door y]
        next step if step[0] != :door || step[1] != $game_map.map_id
        d = PlayBot.find_door($game_map.events.values.map { |e| e.instance_variable_get(:@event) }, step[2])
        d ? [:bump, step[1], d[0], d[1]] : step
      end
      $player.name = PlayBot::NAME
      $player.has_running_shoes = true
      $player.party = [Pokemon.new(:TALONFLAME, 45), Pokemon.new(:ARCANINE, 45), Pokemon.new(:STARAPTOR, 45)]
      Prismfall::LevelCap.disable! if defined?(Prismfall::LevelCap) && Prismfall::LevelCap.respond_to?(:disable!)
      if ["lofts", "backstage"].include?(PlayBot::SESSION)   # these need Tamsin's badge, as on a real save
        n = pfm_gym(:LEADER_TAMSIN) || 2
        $player.badges[n - 1] = true
        $player.badges[(pfm_gym(:LEADER_DORIAN) || 1) - 1] = true
      end
      (101..110).each { |i| $game_switches[i] = true }      # the story so far (Chapters 0-2 flags), as on a real save
      if PlayBot::SESSION.start_with?("house")               # meet N Saltmere townsfolk, beat the aisle actors
        n = PlayBot::SESSION[/\d+/].to_i
        PrismfallPuzzles::AUDIENCE_PEOPLE.keys.first([n, 18].min).each { |k| pfm_audience(k) }
        PrismfallPuzzles.audience_add("quest_EL_LANTERNS", 3) if n > 18
        $game_map.events.each_value { |e| $game_self_switches[[154, e.id, "A"]] = true if e.name[/^Trainer\(/] }
        PrismfallPuzzles.seat_fans
        PlayBot.log("house session: audience #{pf_audience} (#{pf_house_name}), Grand Stage starts at stage #{pf_house_stage}")
      end
      $game_map.need_refresh = true
      PlayBot.recording = true
      PlayBot.log("puzzle session #{PlayBot::SESSION}: start #{st.inspect}; puzzle rooms #{defined?(PrismfallPuzzles) ? PrismfallPuzzles::ROOMS.keys.inspect : 'PLUGIN MISSING'}")
    end
  end
end
