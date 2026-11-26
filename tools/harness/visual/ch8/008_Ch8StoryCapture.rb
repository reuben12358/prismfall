#===============================================================================
# Ch8 story beats on 244 / 249 / 255 in the real engine, dev tool (mapgen/layouts/story_ch8.py + cindervault.py).
#   CH8_STEP 3 on 243: "The Hug" (-> 4, on to 244) -> "My Father" (step stays 4, :gym7_open) -> [Gym 7 is unbuilt:
#   CH8_STEP 5 is set here] -> 240: the Five Bells in the square (-> 6) -> 249: the evacuation -> down to 255: the
#   Caldera Crisis (6, S120, V110) -> 244: "Whose Is It" (:ch8_lightstone, -> 7) -> "Chestnuts" (-> 8) -> 240: "The
#   Herald" (-> 9, S121, V122 1) -> 243: leaving (-> 10, STORY_CHAPTER 9).
# Battles are auto-won; choices come from CH8_CHOICES (0-based, in order: the hug, Sigrun, detonator, caldera branch,
# Light Stone, Larch at the door), default 1,0,1,0,1,2. No frames unless CH8_SHOTS=1 (every 30th; delete frames/ch8_*
# and captures_keep/ch8_* after). RESULT lines in demo.log; a stage that fails stops the run (FAIL).
#   cp maps_out/Data/Map{244,249,255}.rxdata /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch8/008_Ch8StoryCapture.rb --plan ch8story
# The switch / variable names Essentials needs for switch page conditions (S120 on 244) are what the Debug menu's
# "Install Prismfall maps" writes into System.rxdata; this plan puts them into $data_system in memory only.
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch8story")
  module Ch8Cap
    @choices = (ENV["CH8_CHOICES"] || "1,0,1,0,1,2").split(",").map(&:to_i)
    @battles = []
    class << self; attr_accessor :choices, :battles; end
  end
  class << DemoRun
    def c8_run(limit, min = 30)
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

    def c8_idle?; return !$game_system.map_interpreter.running? && !$game_temp.player_transferring && !$game_player.moving?; end

    def c8_fail(msg)
      log("FAIL #{msg}")
      self.auto = false
      stop
      log("done")
      exit
    end

    def c8_goto(map, x, y, dir)
      $game_temp.player_new_map_id = map; $game_temp.player_new_x = x; $game_temp.player_new_y = y
      $game_temp.player_new_direction = dir; $game_temp.player_transferring = true
      c8_run(300, 5) { $game_map.map_id == map && !$game_temp.player_transferring }
    end

    def c8_selfsw(name, ch = "A")
      ev = $game_map.events.values.find { |e| e.name == name }
      return nil if !ev
      return $game_self_switches[[$game_map.map_id, ev.id, ch]]
    end

    def c8_names
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

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch8 story capture boot ok; choices #{Ch8Cap.choices.inspect}")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      c8_names
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 45, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 45, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      $game_variables[129] = 3
      $game_map.setup(243)
      $game_player.moveto(20, 19); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = 30
      record("ch8_story") if ENV["CH8_SHOTS"] == "1"
      self.auto = true
      t0 = System.uptime
      # --- "The Hug" (243) -> 244, then "My Father"
      f = c8_run(5000) { $game_map.map_id == 244 && $game_variables[129] >= 4 }
      log("RESULT the hug: CH8_STEP=#{$game_variables[129]} map=#{$game_map.map_id} frames=#{f}")
      c8_fail("The Hug did not reach 244") if $game_map.map_id != 244
      f = c8_run(5000) { c8_selfsw("My Father") && c8_idle? }
      log("RESULT my father: CH8_STEP=#{$game_variables[129]} selfA=#{c8_selfsw('My Father').inspect} gym7_open=#{pfm_get(:gym7_open).inspect} " \
          "pos=#{$game_player.x},#{$game_player.y} brann_opacity=#{$game_map.events.values.find { |e| e.name == 'Brann' }&.opacity} frames=#{f}")
      c8_fail("My Father did not finish") if !c8_selfsw("My Father") || $game_variables[129] != 4
      # --- Gym 7 won (unbuilt: set here): CH8_STEP 5, the Five Bells in the square, then down to the Slag Ward
      $game_variables[129] = 5
      c8_goto(240, 21, 4, 2)
      f = c8_run(4000) { $game_variables[129] >= 6 && c8_idle? }
      log("RESULT five bells (240): CH8_STEP=#{$game_variables[129]} pos=#{$game_player.x},#{$game_player.y} tone=#{$game_screen.tone.red.round} frames=#{f}")
      c8_fail("the square's Five Bells did not reach 6") if $game_variables[129] < 6
      c8_goto(249, 6, 9, 6)
      f = c8_run(3000) { c8_selfsw("Five Bells (ward)") && !$game_system.map_interpreter.running? }
      c8_run(240, 240) { false }                       # let the families walk off
      gone = %w[Evacuee\ 1 Evacuee\ 2 Evacuee\ 3 Evacuating\ Mother Child\ with\ Litwick\ Jar].map do |n|
        e = $game_map.events.values.find { |x| x.name == n }
        "#{n}:#{e&.x},#{e&.y},o#{e&.opacity}"
      end
      log("RESULT five bells: selfA=#{c8_selfsw('Five Bells (ward)').inspect} tone=#{$game_screen.tone.red.round} evacuees=#{gone.inspect} frames=#{f}")
      c8_fail("the ward's Five Bells did not play") if !c8_selfsw("Five Bells (ward)")
      # --- down the tap stair: the crisis, then 244
      c8_goto(255, 13, 18, 8)
      f = c8_run(12000) { $game_variables[129] >= 7 && $game_map.map_id == 244 }
      log("RESULT crisis+lightstone: CH8_STEP=#{$game_variables[129]} S120=#{$game_switches[120]} V110=#{$game_variables[110]} " \
          "ch8_caldera=#{pf_choice(:ch8_caldera).inspect} ch8_lightstone=#{pf_choice(:ch8_lightstone).inspect} map=#{$game_map.map_id} " \
          "battles=#{Ch8Cap.battles.inspect} frames=#{f}")
      c8_fail("never reached CH8_STEP 7 on 244") if $game_variables[129] < 7
      # --- "Chestnuts"
      f = c8_run(6000) { $game_variables[129] >= 8 && c8_idle? && $game_screen.tone.red > -100 }
      left = $game_map.events.values.select { |e| e.character_name.to_s != "" && e.opacity > 0 }.map(&:name)
      log("RESULT chestnuts: CH8_STEP=#{$game_variables[129]} map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} " \
          "tone=#{$game_screen.tone.red.round} shown=#{left.inspect} frames=#{f}")
      # --- next morning: up to the square, "The Herald"; then out through the gate
      c8_goto(240, 20, 26, 8)
      f = c8_run(6000) { $game_variables[129] >= 9 && c8_idle? }
      log("RESULT herald: CH8_STEP=#{$game_variables[129]} S121=#{$game_switches[121]} V122=#{$game_variables[122]} " \
          "column=#{%w[Herald Standard-bearer].map { |n| e = $game_map.events.values.find { |x| x.name == n }; "#{n}:#{e&.x},#{e&.y},o#{e&.opacity}" }.inspect} frames=#{f}")
      c8_fail("The Herald did not reach 9") if $game_variables[129] < 9
      c8_goto(243, 34, 6, 2)
      f = c8_run(3000) { $game_variables[129] >= 10 && c8_idle? }
      log("RESULT leaving: CH8_STEP=#{$game_variables[129]} STORY_CHAPTER=#{$game_variables[102]} quest=#{($PokemonGlobal.pf_quests[:eighteen_roads] rescue nil).inspect} " \
          "frames=#{f} secs=#{(System.uptime - t0).round(1)}")
      c8_run(60, 60) { true }
      self.auto = false
      stop
      log("done")
    end
  end
  module Input
    class << self
      alias c8_trigger? trigger? unless method_defined?(:c8_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return c8_trigger?(button)
      end
    end
  end
  alias c8_pbShowCommands pbShowCommands unless defined?(c8_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = Ch8Cap.choices.shift || 0
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return c8_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias c8_pbCommandPhase pbCommandPhase unless method_defined?(:c8_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        DemoRun.log("battle vs #{names.join(' + ')}")
        Ch8Cap.battles << names
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      c8_pbCommandPhase
    end
  end
end
