#===============================================================================
# DEV-ONLY: puzzle sessions for the playtest bot (run_puzzles.sh; never ship).
# The bot walks into a gym through its town door and solves the puzzle rooms with
# ordinary input only: arrow keys along BFS paths, Use on levers/ropes, walking
# into spools.  Nothing sets a switch or variable for it.
#   PLAYBOT_SESSION=gym1   map 120's gym door -> the Loomhouse hall (one heddle) -> the Warden
#   PLAYBOT_SESSION=lofts  the optional Upper Lofts: Weaving Hall -> Canopy Lofts -> Granny's Knot
#   PLAYBOT_SESSION=gym2   Saltmere Old Town door -> Foyer -> Revolving Stage <-> Fly Loft -> the Grand Stage
# New step kinds: [:use_from, map, x, y, dir]  stand on (x, y), face dir, press Use
#                 [:ride, map, x, y, dir]      stand on (x, y), walk into the thing in dir until thrown elsewhere
#                 [:shot, map, "name"]         screenshot when the map is idle
#===============================================================================
module PlayBot
  PUZZLE_START = { "gym1" => [120, 36, 13], "lofts" => [130, 9, 21], "gym2" => [147, 53, 24], "d1" => [522, 6, 36] }
  # Gym 1 (SPINE Rev 13): one easy hall. One heddle, one pull, two trainers, the Warden.
  GYM1_PLAN = [
    [:shot, 120, "g1_00_outside_the_loomhouse"],
    [:bump, 120, 36, 12],                 # the elder tree's door
    [:shot, 130, "g1_01_hall_start"],
    [:goto, 130, 9, 12], [:shot, 130, "g1_02_at_the_loom_bed"],
    [:talk, 130, 11, 10], [:shot, 130, "g1_03_heddle_pulled"],
    [:goto, 130, 9, 9],  [:shot, 130, "g1_04_on_the_plank"],
    [:goto, 130, 9, 6],  [:shot, 130, "g1_05_before_the_warden"],
    [:done]
  ]
  # The optional Upper Lofts (open after Badge 1): linked heddles, spools and the brass wire, Granny's Knot.
  LOFTS_PLAN = [
    [:talk, 130, 11, 10],
    [:goto, 130, 15, 3], [:shot, 130, "lf_00_stairs_to_the_upper_lofts"],
    [:goto, 130, 15, 2],
    [:shot, 131, "lf_01_hall_start"],
    [:talk, 131, 1, 21],  [:shot, 131, "lf_02_hall_red"],
    [:talk, 131, 9, 21],  [:shot, 131, "lf_03_hall_gold"],
    [:talk, 131, 23, 21], [:shot, 131, "lf_04_hall_green_all_right"],
    [:goto, 131, 21, 18], [:shot, 131, "lf_05_hall_on_the_planks"],
    [:goto, 131, 21, 4],
    [:goto, 131, 12, 1],
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
  GYM2_PLAN = [
    [:shot, 147, "g2_00_outside_the_playhouse"],
    [:bump, 147, 53, 23],
    [:shot, 150, "g2_01_foyer_start"],
    [:use_from, 150, 3, 6, 6], [:shot, 150, "g2_02_foyer_overture"],
    [:goto, 150, 9, 2],
    [:shot, 151, "g2_03_stage_work_lights"],
    [:use_from, 151, 2, 17, 2], [:shot, 151, "g2_04_stage_shipwreck"],
    [:goto, 151, 4, 13], [:shot, 151, "g2_05_stage_across_the_gangplank"],
    [:use_from, 151, 6, 10, 6], [:shot, 151, "g2_06_stage_forest"],
    [:goto, 151, 2, 4],
    [:shot, 152, "g2_07_loft_start"],
    [:talk, 152, 21, 6], [:shot, 152, "g2_08_loft_rope2"],
    [:talk, 152, 22, 6], [:shot, 152, "g2_09_loft_rope3"],
    [:goto, 152, 22, 4],
    [:shot, 151, "g2_10_stage_right_side"],
    [:use_from, 151, 18, 5, 8], [:shot, 151, "g2_11_stage_throne"],
    [:goto, 151, 14, 10], [:shot, 151, "g2_12_stage_through_flat_b"],
    [:goto, 151, 12, 7],  [:shot, 151, "g2_13_stage_on_the_rostrum"],
    [:goto, 151, 12, 2],
    [:arrive, 154], [:shot, 154, "g2_14_the_grand_stage"],
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

  class << self
    alias puz_plan plan unless method_defined?(:puz_plan)
    def plan
      return GYM1_PLAN if SESSION == "gym1"
      return GYM2_PLAN if SESSION == "gym2"
      return LOFTS_PLAN if SESSION == "lofts"
      return D1_PLAN if SESSION == "d1"
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
      if st
        PrismfallMaps.define_singleton_method(:apply_start_position) do
          $data_system.start_map_id, $data_system.start_x, $data_system.start_y = *st
          true
        end
      end
      puzbot_start_new
      return if !st
      $player.name = PlayBot::NAME
      $player.has_running_shoes = true
      $player.party = [Pokemon.new(:TALONFLAME, 45), Pokemon.new(:ARCANINE, 45), Pokemon.new(:STARAPTOR, 45)]
      Prismfall::LevelCap.disable! if defined?(Prismfall::LevelCap) && Prismfall::LevelCap.respond_to?(:disable!)
      $player.badges[0] = true if PlayBot::SESSION == "lofts"
      (101..110).each { |i| $game_switches[i] = true }      # the story so far (Chapters 0-2 flags), as on a real save
      $game_map.need_refresh = true
      PlayBot.recording = true
      PlayBot.log("puzzle session #{PlayBot::SESSION}: start #{st.inspect}; puzzle rooms #{defined?(PrismfallPuzzles) ? PrismfallPuzzles::ROOMS.keys.inspect : 'PLUGIN MISSING'}")
    end
  end
end
