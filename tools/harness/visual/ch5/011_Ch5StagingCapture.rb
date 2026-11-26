#===============================================================================
# Ch5 stage-direction pass (bracketed narration played, not printed) in the real engine, dev tool.
# Group "lowlight" (180 / 181 / 608, mapgen/layouts/story_ch5.py) and group "spire" (582 / 186 / 951,
# mapgen/layouts/lumen_interiors.py): each scene runs from its event; RESULT lines say whether it finished and what
# it left behind (steps, switches, who is still shown). Battles are auto-won, choices take CH5S_CHOICES (0-based,
# default 1 for the Testimony). No frames unless CH5S_SHOTS=1 (every 30th; delete frames/ch5_* and
# captures_keep/ch5_* after). Switch names go into $data_system in memory (the Debug installer's job).
#   cp maps_out/Data/Map{180,181,608,582,186,951}.rxdata /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch5/011_Ch5StagingCapture.rb --plan ch5stage_lowlight
#   ... --plan ch5stage_spire
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch5stage")
  module C5S
    @choices = (ENV["CH5S_CHOICES"] || "1").split(",").map(&:to_i)
    @battles = []
    class << self; attr_accessor :choices, :battles; end
  end
  class << DemoRun
    def s_run(limit, min = 20)
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > limit
        break if f > min && yield
      end
      return f
    end

    def s_idle?; return !$game_system.map_interpreter.running? && !$game_temp.player_transferring && !$game_player.moving?; end
    def s_ev(name); return $game_map.events.values.find { |e| e.name == name }; end
    def s_selfsw(name, ch = "A"); e = s_ev(name); return e ? $game_self_switches[[$game_map.map_id, e.id, ch]] : nil; end
    def s_shown(*names); return names.map { |n| e = s_ev(n); "#{n}:#{e ? "#{e.x},#{e.y},o#{e.opacity},#{e.character_name}" : 'none'}" }; end

    def s_map(id, x, y, dir = 2)
      $game_map.setup(id)
      $game_player.moveto(x, y)
      $game_player.direction = dir
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.autoplay
      $game_map.need_refresh = true
      s_run(30, 30) { false }
    end

    # runs an event's current page like pressing USE on it, then waits for the map to settle
    def s_talk(name, limit = 4000)
      e = s_ev(name)
      return log("no event #{name}") if !e
      e.refresh
      $game_system.map_interpreter.setup(e.list, e.id) if e.list
      s_run(limit) { s_idle? }
    end

    def s_autorun(limit = 6000)
      s_run(limit, 40) { s_idle? }
    end

    def s_names
      File.foreach("Data/system_prismfall.txt") do |l|
        next if l.start_with?("#")
        kind, id, name = l.chomp.split("\t", 3)
        next if !name
        list = (kind == "S") ? $data_system.switches : $data_system.variables
        list[id.to_i] = name if list[id.to_i].to_s.empty?
      end
    rescue StandardError => e
      log("names: #{e.message}")
    end

    def lowlight
      # --- 180: arrival (the camera and the airship's shadow), then the grille
      $game_variables[125] = 3
      s_map(180, 6, 59, 8)
      f = s_autorun
      log("RESULT 180 arrival: selfA=#{s_selfsw('Arrival').inspect} display=#{$game_map.display_x},#{$game_map.display_y} frames=#{f}")
      $game_player.moveto(74, 39); $game_player.turn_up
      s_run(20, 20) { false }
      f = s_talk("Nadir Kid")
      log("RESULT 180 grille: kid_selfA=#{s_selfsw('Nadir Kid').inspect} #{s_shown('Nadir Kid', 'Zenith Officer').inspect} frames=#{f}")
      # --- 181: Dex and Spark, Rook's blackout, the lights back
      s_map(181, 4, 9, 8)
      f = s_talk("Dex")
      log("RESULT 181 dex: CH5_STEP=#{$game_variables[125]} #{s_shown('Spark the Pichu').inspect} frames=#{f}")
      $game_player.moveto(28, 19); $game_player.turn_up
      f = s_talk("Rook")
      boxes = (1..4).map { |i| s_ev("Junction box #{i}")&.tile_id }
      log("RESULT 181 blackout: S424=#{$game_switches[424]} rook_selfA=#{s_selfsw('Rook').inspect} box_tiles=#{boxes.inspect} " \
          "tone=#{$game_screen.tone.red.round} frames=#{f}")
      $game_switches[423] = true
      $game_map.need_refresh = true
      f = s_autorun
      log("RESULT 181 lights back: CH5_STEP=#{$game_variables[125]} S424=#{$game_switches[424]} tone=#{$game_screen.tone.red.round} " \
          "#{s_shown('Nessa', 'Old Jory', 'Benno').inspect} frames=#{f}")
      # --- 608: the aftermath, Valen, Voss, the testimony
      $game_variables[125] = 9
      s_map(608, 3, 6, 2)
      f = s_autorun
      log("RESULT 608 aftermath: selfA=#{s_selfsw('Aftermath').inspect} tone=#{$game_screen.tone.red.round},#{$game_screen.tone.blue.round} frames=#{f}")
      $game_player.moveto(2, 6); $game_player.turn_left
      f = s_talk("Valen at the Veil")
      log("RESULT 608 valen: CH5_STEP=#{$game_variables[125]} valen_dir=#{s_ev('Valen at the Veil')&.direction} frames=#{f}")
      f = s_talk("Voss with the crate")
      f2 = s_talk("Testimony")
      log("RESULT 608 testimony: CH5_STEP=#{$game_variables[125]} S115=#{$game_switches[115]} choice=#{pf_choice(:ch5_lowlight_testimony).inspect} frames=#{f}+#{f2}")
    end

    def spire
      # --- 582: the scanner (Juno green, you NULL, the brass tube)
      $game_variables[125] = 2
      s_map(582, 8, 10, 8)
      f = s_talk("Scanner")
      log("RESULT 582 scanner: CH5_STEP=#{$game_variables[125]} invitation=#{(pfm_has?(:GALAINVITATION) rescue '?').inspect} " \
          "guard_dir=#{s_ev('Meridian Security')&.direction} frames=#{f}")
      # --- 186: the gala opening, Valen, the window, then the replica -> the speech -> the raid
      $game_variables[125] = 6
      s_map(186, 13, 18, 8)
      f = s_autorun
      log("RESULT 186 opening: CH5_STEP=#{$game_variables[125]} display=#{$game_map.display_x},#{$game_map.display_y} " \
          "#{s_shown('Rook (gala)', 'Juno (gala)', 'Larch (gala)').inspect} frames=#{f}")
      $game_player.moveto(4, 8); $game_player.turn_up
      f = s_talk("Valen")
      log("RESULT 186 valen: dir=#{s_ev('Valen')&.direction} frames=#{f}")
      $game_player.moveto(25, 9); $game_player.turn_left
      f = s_talk("Atrium window")
      $game_player.moveto(13, 6); $game_player.turn_up
      s_run(10, 10) { false }
      f = s_talk("Replica", 9000)
      lift = s_ev("Service lift")
      log("RESULT 186 raid: CH5_STEP=#{$game_variables[125]} battles=#{C5S.battles.length} lift_tile=#{lift&.tile_id} " \
          "#{s_shown('Thistle (raid)', 'Hollis', 'Quent', 'Rook (gala)', 'Voss').inspect} tone=#{$game_screen.tone.red.round} frames=#{f}")
      # --- 951: Rook on the stair
      $game_variables[125] = 8
      s_map(951, 10, 11, 2)
      $game_player.move_down
      f = s_run(3000, 40) { s_idle? }
      log("RESULT 951 rook: selfA=#{s_selfsw('Rook catches up').inspect} #{s_shown('Rook (stair)').inspect} pos=#{$game_player.x},#{$game_player.y} frames=#{f}")
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      group = ENV["DEMO_PLAN"].to_s.sub("ch5stage_", "")
      log("ch5 staging capture boot ok: #{group}")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      s_names
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:MARSHTOMP, 30, [:SURF, :MUDSHOT, :ICEBEAM, :PROTECT])]
      self.every = 30
      record("ch5_stage_#{group}") if ENV["CH5S_SHOTS"] == "1"
      self.auto = true
      t0 = System.uptime
      (group == "spire") ? spire : lowlight
      log("RESULT done in #{(System.uptime - t0).round(1)} s")
      self.auto = false
      stop
      log("done")
    end
  end
  module Input
    class << self
      alias c5s_trigger? trigger? unless method_defined?(:c5s_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return c5s_trigger?(button)
      end
    end
  end
  alias c5s_pbShowCommands pbShowCommands unless defined?(c5s_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = C5S.choices.shift || 0
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return c5s_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias c5s_pbCommandPhase pbCommandPhase unless method_defined?(:c5s_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        DemoRun.log("battle vs #{(@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }.inspect} wild=#{@battlers.compact.select(&:opposes?).map(&:species).inspect}")
        C5S.battles << 1
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      c5s_pbCommandPhase
    end
  end
end
