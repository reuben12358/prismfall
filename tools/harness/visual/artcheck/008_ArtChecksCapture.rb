#===============================================================================
# Art checks in the real engine (dev tool; Gemini's 2026-11-26 delivery, integration handoff §3).
#   1. the player's movement sheets (Core 026_PlayerLooks.rb): walk, run, bike, surf, fishing and surf-fishing,
#      for PLAYER_A and PLAYER_B, on Brinecut Mine B1F (545) at the salt-lake shore;
#   2. map 545 itself with the Gen 5 reskin (the salt shore);
#   3. a cameo VS screen (Venam, v1) and a Grounds Ladder class intro (Wyrm Rider Tova, new 16-frame strip).
# Single screenshots (Captures/intro_artcheck/*.bmp) plus sparse battle frames (every 30th); RESULT lines in demo.log.
#   cp maps_out/Data/Map545.rxdata maps_out/Data/system_prismfall.txt /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture "$PWD/tools/harness/visual/artcheck/008_ArtChecksCapture.rb" --plan artcheck
# Delete /home/claude/run_intro/frames/intro_artcheck* and captures_keep/intro_artcheck* after looking.
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("artcheck")
  class << DemoRun
    AC_DIR = "#{DemoRun::ROOT}/intro_artcheck"

    def ac_shot(name)
      Dir.mkdir(AC_DIR) if !Dir.exist?(AC_DIR)
      Graphics.screenshot("#{AC_DIR}/#{name}.bmp")
      log("shot #{name}: charset=#{$game_player.character_name} pattern=#{$game_player.pattern} " \
          "dir=#{$game_player.direction} at #{$game_player.x},#{$game_player.y}")
    end

    def ac_run(frames)
      frames.times do
        Graphics.update; Input.update
        $scene.update
      end
    end

    def ac_map(id, x, y, dir = 2)
      $game_map.setup(id)
      $game_player.moveto(x, y)
      $game_player.direction = dir
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      $game_screen.start_tone_change(Tone.new(0, 0, 0, 0), 0) rescue nil
      ac_run(20)
      if ENV["AC_DARK"] != "1"                      # even Flash leaves the corners dark: hide the darkness for the shots
        ds = $game_temp.darkness_sprite
        ds.visible = false if ds && !ds.disposed?
      end
    end

    def ac_water?(x, y)
      return false if !$game_map.valid?(x, y)
      return $game_map.terrain_tag(x, y).can_surf_freely rescue $game_map.terrain_tag(x, y).can_surf
    end

    # a land tile you can stand on: passable both ways, no event on it
    def ac_floor?(x, y)
      return false if !$game_map.valid?(x, y) || ac_water?(x, y)
      return false if $game_map.events.values.any? { |e| e.x == x && e.y == y && !e.through }
      return $game_map.passable?(x, y, 4) && $game_map.passable?(x, y, 6)
    end

    # a water tile with two more water tiles east of it and three clear floor tiles west of it, as central as possible
    def ac_shore
      best = nil
      cx = $game_map.width / 2.0; cy = $game_map.height / 2.0
      (2...$game_map.height - 2).each do |y|
        (4...$game_map.width - 3).each do |x|
          next if !ac_water?(x, y) || !ac_water?(x + 1, y) || !ac_water?(x + 2, y)
          next if (1..3).any? { |d| !ac_floor?(x - d, y) }
          score = ((x - cx)**2) + ((y - cy)**2)
          best = [score, x, y] if !best || score < best[0]
        end
      end
      return best ? best[1..2] : nil
    end

    def ac_reset_player
      $PokemonGlobal.surfing = false
      $PokemonGlobal.bicycle = false
      $game_player.lock_pattern = false
      $game_player.through = true                  # the walks below ignore passability
      $game_player.charsetData = nil
      $game_player.refresh_charset
    end

    # n tiles in direction dir, a shot every `every` frames while moving
    def ac_walk(tag, dir, tiles, every = 6)
      i = 0
      tiles.times do
        case dir
        when 4 then $game_player.move_left
        when 6 then $game_player.move_right
        when 2 then $game_player.move_down
        else        $game_player.move_up
        end
        f = 0
        loop do
          Graphics.update; Input.update
          $scene.update
          f += 1
          if f % every == 0 && i < 3
            ac_shot("#{tag}_#{i}"); i += 1
          end
          break if !$game_player.moving? || f > 60
        end
      end
    end

    def ac_looks(sx, sy)
      [1, 2].each do |look|
        tag = (look == 1) ? "A" : "B"
        pbChangePlayer(look)
        ac_reset_player
        meta = GameData::PlayerMetadata.get(look)
        log("RESULT look #{tag} sheets: " + %i[walk_charset run_charset cycle_charset surf_charset dive_charset fish_charset
                                                surf_fish_charset].map { |k| "#{k}=#{meta.send(k)}" }.join(" "))
        fish_only = (ENV["AC_PARTS"] || "").split(",").include?("fish")
        if !fish_only
        # land, three tiles west of the shore
        $game_player.moveto(sx - 3, sy); $game_player.turn_down
        $game_player.charsetData = nil; $game_player.refresh_charset
        ac_run(10)
        ac_shot("#{tag}1_walk_stand")
        # run east two tiles then back
        $player.has_running_shoes = true
        $PokemonSystem.runstyle = 1
        ac_walk("#{tag}2_run", 6, 2, 4)
        $PokemonSystem.runstyle = 0
        ac_run(10)
        $game_player.moveto(sx - 3, sy)
        # bike
        $PokemonGlobal.bicycle = true
        $game_player.charsetData = nil; $game_player.refresh_charset
        ac_run(4)
        ac_shot("#{tag}3_bike_stand")
        ac_walk("#{tag}3_bike", 6, 2, 4)
        $PokemonGlobal.bicycle = false
        end
        # fishing on land, facing the water
        $game_player.moveto(sx - 1, sy); $game_player.turn_right
        $game_player.charsetData = nil; $game_player.refresh_charset
        ac_run(6)
        $game_player.set_movement_type(:fishing)
        $game_player.lock_pattern = true
        [3, 1, 0].each do |p|
          $game_player.pattern = p
          ac_run(4)
          ac_shot("#{tag}4_fish_p#{p}")
        end
        $game_player.lock_pattern = false
        $game_player.set_movement_type(:walking_stopped)
        # surf: onto the water, two tiles east
        $game_player.moveto(sx, sy); $game_player.turn_right
        $PokemonGlobal.surfing = true
        $game_player.charsetData = nil; $game_player.refresh_charset
        ac_run(12)
        ac_shot("#{tag}5_surf_stand")
        ac_walk("#{tag}5_surf", 6, 1, 5) if !fish_only
        ac_run(12)                                     # settle first: a step that just ended resets the sheet
        # surf-fishing
        $game_player.set_movement_type(:surf_fishing)
        $game_player.lock_pattern = true
        $game_player.pattern = 0
        ac_run(4)
        ac_shot("#{tag}6_surffish")
        ac_reset_player
      end
    end

    def ac_battle_intro(name, &block)
      party = [DemoRun.mon(:SAMUROTT, 50, [:SURF, :RAZORSHELL]), DemoRun.mon(:ARCANINE, 50, [:FLAMETHROWER])]
      self.every = (ENV["AC_EVERY"] || "30").to_i
      DemoRun.battle("intro_artcheck_#{name}", party, :turns => 0) do
        setBattleRule("canLose")
        block.call
      end
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("artcheck boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      $scene.createSpritesets
      # miniupdate only: a full update would start the new-game autorun on the start map (the intro), whose
      # messages wait for input this plan never gives
      30.times { Graphics.update; $scene.miniupdate }
      log("new game ok (map #{$game_map.map_id})")
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:OSHAWOTT) rescue nil
      pbChangePlayer(1)
      parts = (ENV["AC_PARTS"] || "map,looks,vs").split(",")
      shore = nil
      begin
        $game_system.map_interpreter.clear rescue nil
        # 545 is a dark cave (a small light circle until Flash): light it so the tiles can be judged
        $PokemonGlobal.flashUsed = true if ENV["AC_DARK"] != "1"
        ac_map(545, 10, 10)
        log("on 545")
        shore = ac_shore
        log("RESULT 545: size #{$game_map.width}x#{$game_map.height} tileset #{$game_map.tileset_id} shore #{shore.inspect}")
        if shore
          $game_player.moveto(shore[0] - 1, shore[1]); $game_player.turn_right
          $game_player.charsetData = nil; $game_player.refresh_charset
          ac_run(20)
          ac_shot("M1_545_shore") if parts.include?("map")
        end
        if parts.include?("map")
          # the lake's middle, from its widest stretch of water
          xs = (0...$game_map.width).select { |x| ac_water?(x, shore ? shore[1] : 10) }
          $game_player.moveto(xs.empty? ? 10 : xs[xs.length / 2], shore ? shore[1] : 10)
          $PokemonGlobal.surfing = !xs.empty?
          $game_player.charsetData = nil; $game_player.refresh_charset
          ac_run(20)
          ac_shot("M2_545_lake")
          $PokemonGlobal.surfing = false
        end
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        log("EXCEPTION map #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(10).join("\n  "))
      end
      if (parts.include?("looks") || parts.include?("fish")) && shore
        begin
          ac_looks(*shore)
        rescue Exception => e
          raise if e.is_a?(SystemExit)
          log("EXCEPTION looks #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(10).join("\n  "))
        end
      end
      if parts.include?("vs")
        pbChangePlayer(1)
        ac_reset_player
        $game_player.through = false
        $game_player.moveto(shore ? shore[0] - 2 : 10, shore ? shore[1] : 10)
        ac_run(10)
        ac_battle_intro("venam") { TrainerBattle.start(:FESTIVAL_VENAM, "Venam", 1) }
        ac_battle_intro("tova") { TrainerBattle.start(:WYRM_RIDER, "Tova") }
      end
      log("done")
    end
  end

  module PBDayNight
    class << self
      def isNight?(*a);   false; end
      def isEvening?(*a); false; end
      def isMorning?(*a); false; end
      def isDay?(*a);     true;  end
    end
  end

  # the battles stop at the first command phase, after the VS screen and both send-outs
  class Battle
    alias ac_pbCommandPhase pbCommandPhase unless method_defined?(:ac_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        DemoRun.log("command phase reached: foe #{(@opponent || []).map { |t| "#{t.trainer_type} #{t.name}" }.inspect}")
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 3
        return
      end
      ac_pbCommandPhase
    end
  end
end
