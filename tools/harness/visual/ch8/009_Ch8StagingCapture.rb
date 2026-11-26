#===============================================================================
# Ch8 stage directions (240 / 243 / 249 guarded exits and NPCs, story_ch8.py STAGE) and 185's Prism Arena model
# vignette (019_Vignettes.rb) in the real engine, dev tool. Each event runs as if touched / talked to; RESULT lines
# say it finished and where it left the player. CH8S_SHOTS=1 records the arena vignette only (every 10th frame;
# delete frames/ch8_* and captures_keep/ch8_* after looking).
#   cp maps_out/Data/Map{185,240,243,249}.rxdata /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch8/009_Ch8StagingCapture.rb --plan ch8stage
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch8stage")
  class << DemoRun
    def g_run(limit, min = 20)
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

    def g_idle?; return !$game_system.map_interpreter.running? && !$game_temp.player_transferring && !$game_player.moving?; end
    def g_ev(name); return $game_map.events.values.find { |e| e.name == name }; end

    def g_map(id, x, y, dir)
      $game_map.setup(id)
      $game_player.moveto(x, y)
      $game_player.direction = dir
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      g_run(20, 20) { false }
    end

    def g_event(name, x, y, dir, limit = 2000)
      $game_player.moveto(x, y)
      $game_player.direction = dir
      e = g_ev(name)
      return "#{name}: no event" if !e
      e.refresh
      $game_system.map_interpreter.setup(e.list, e.id) if e.list
      t0 = System.uptime
      f = g_run(limit) { g_idle? }
      return "#{name}: frames=#{f} secs=#{(System.uptime - t0).round(1)} pos=#{$game_player.x},#{$game_player.y} dir=#{$game_player.direction}"
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch8 staging capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $player.party = [DemoRun.mon(:SWAMPERT, 45, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT])]
      self.every = 10
      self.auto = true
      g_map(185, 12, 8, 8)
      record("ch8_stage_arena") if ENV["CH8S_SHOTS"] == "1"
      e = g_ev("Arena model")
      log("RESULT 185 #{g_event('Arena model', e.x, e.y + 1, 8)}")
      stop
      $game_variables[129] = 4
      g_map(240, 20, 3, 8)
      log("RESULT 240 #{g_event('To The Foundry (Gym 7)', 20, 2, 8)}")
      log("RESULT 240 #{g_event('To Pyre Keep Rampart', g_ev('To Pyre Keep Rampart').x, g_ev('To Pyre Keep Rampart').y, 8)}")
      log("RESULT 240 #{g_event('To The Dragon Roosts', 38, 2, 8)}")
      log("RESULT 240 #{g_event('To The Ashmarch', 1, 24, 4)}")
      log("RESULT 240 #{g_event('Old Smith', 35, 38, 8)}")
      g_map(243, 18, 21, 2)
      log("RESULT 243 #{g_event('To The Pyre Road', 18, 22, 2)}")
      w = g_ev("To The Ashmarch")
      log("RESULT 243 #{g_event('To The Ashmarch', w.x, w.y, 4)}") if w
      g_map(249, 15, 14, 8)
      log("RESULT 249 #{g_event('Child with Litwick Jar', 15, 14, 8)} jar_opacity=#{g_ev('Litwick jar')&.opacity}")
      self.auto = false
      log("done")
    end
  end
  module Input
    class << self
      alias g8_trigger? trigger? unless method_defined?(:g8_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return g8_trigger?(button)
      end
    end
  end
end
