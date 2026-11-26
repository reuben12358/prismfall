#===============================================================================
# Ch5 -> Act II: Larch at 3 a.m. (952) and Interlude I "Lamplight" (182 -> 106 -> 105 -> 106 -> 182) in the real
# engine, dev tool. Plays from CH5_STEP 11: the staged vault scene (-> 12), the hand-over in the Center (the swap to
# Kestrel, the title card), the lamp room, the trunk / memory flash / Haunter (the first battle is LOST on purpose
# to walk the "restarts at the stair" loop, the second is won), the bag, Edda's boat, the goodbye, END OF ACT I.
# RESULT lines in demo.log: party swapped and restored, V119, CH5_STEP 13, STORY_ACT 2, STORY_CHAPTER 6, S162.
#   cp maps_out/Data/Map{105,106,182,952}.rxdata /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch5/010_LamplightCapture.rb --plan lamplight
#   LAMP_SAFE=1 = photosensitive. NO frames are recorded by default (the RESULT lines are the check). To look:
#   LAMP_SHOTS=memory (the trunk -> the first battle only) or LAMP_SHOTS=all, LAMP_EVERY=n (default 30). A frame is
#   0.8 MB and run_intro keeps every frame twice (frames/ and captures_keep/): delete both folders after looking.
#   A stage that fails stops the run at once (FAIL line) instead of waiting out the later stages.
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("lamplight")
  module LampCap
    @battles = []
    @lines = 0
    class << self; attr_accessor :battles, :lines; end
  end
  class << DemoRun
    def lamp_run(limit, min = 30)
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

    def lamp_fail(msg)
      log("FAIL #{msg}")
      self.auto = false
      stop
      log("done")
      exit
    end

    def lamp_idle?; return !$game_system.map_interpreter.running? && !$game_temp.player_transferring; end

    def lamp_party
      return $player.party.map { |p| "#{p.name}/#{p.species}/L#{p.level}" }.join(" ")
    end

    def lamp_goto(map, x, y, dir)
      $game_temp.player_new_map_id = map; $game_temp.player_new_x = x; $game_temp.player_new_y = y
      $game_temp.player_new_direction = dir; $game_temp.player_transferring = true
      lamp_run(300, 20) { $game_map.map_id == map && lamp_idle? }
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("lamplight capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      Prismfall::Cutscene.photosensitive = (ENV["LAMP_SAFE"] == "1") if defined?(Prismfall::Cutscene)
      $player.party = [DemoRun.mon(:MARSHTOMP, 30, [:SURF, :MUDSHOT, :ICEBEAM, :PROTECT]),
                       DemoRun.mon(:LUXIO, 29, [:SPARK, :BITE, :CHARGE, :ROAR])]
      own = $player.party.map { |p| p.personalID }
      $player.party[0].hp = 7                      # a night's sleep at the Center should mend this
      $game_variables[125] = 11
      $game_map.setup(952)
      $game_player.moveto(18, 16); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = [(ENV["LAMP_EVERY"] || "30").to_i, 10].max
      shots = ENV["LAMP_SHOTS"].to_s
      record("ch5_lamplight") if shots == "all"
      self.auto = true
      t0 = System.uptime
      # --- Larch at 3 a.m. -> bed -> the hand-over -> the lamp room's opening
      f = lamp_run(6000) { $game_variables[125] >= 12 && $game_map.map_id == 106 && lamp_idle? }
      log("RESULT larch+handover: CH5_STEP=#{$game_variables[125]} V119=#{$game_variables[119]} map=#{$game_map.map_id} " \
          "pos=#{$game_player.x},#{$game_player.y} name=#{$player.name} charset=#{$game_player.character_name} " \
          "party=[#{lamp_party}] interlude=#{Prismfall::Interlude.active?(1)} tone=#{$game_screen.tone.red.round} frames=#{f}")
      lamp_fail("the hand-over never reached the lamp room") if $game_map.map_id != 106 || $game_variables[119] != 1
      ev = $game_map.events.values.find { |e| e.name == "Hesper Vane" }
      log("hesper page graphic=#{ev&.character_name} dir=#{ev&.direction} list=#{ev&.list&.length}")
      # --- down the stairs (the warp), the trunk
      lamp_goto(105, 10, 7, 2)
      log("105: pos=#{$game_player.x},#{$game_player.y} tone=#{$game_screen.tone.red.round} bgm=#{$game_system.playing_bgm&.name.inspect}")
      # the night door: walking onto the mat's approach bumps him back
      $game_player.moveto(8, 11)
      $game_player.move_left
      lamp_run(200, 20) { !$game_player.moving? && lamp_idle? }
      log("RESULT night door: pos=#{$game_player.x},#{$game_player.y} (stepped onto 7,11; pushed back to 8,11 expected)")
      $game_player.moveto(8, 11); $game_player.turn_up
      tr = $game_map.events.values.find { |e| e.name == "Trunk" }
      log("trunk event #{tr&.id} list #{tr&.list&.length}")
      lamp_fail("no Trunk interlude page") if !tr || tr.list.length < 20
      record("ch5_lamplight") if shots == "memory"
      $game_system.map_interpreter.setup(tr.list, tr.id)
      f = lamp_run(12000) { PrismfallMaps.flags[:il1_packed] && lamp_idle? }
      lamp_fail("the trunk scene never finished") if !PrismfallMaps.flags[:il1_packed]
      log("RESULT trunk: packed=#{PrismfallMaps.flags[:il1_packed].inspect} battles=#{LampCap.battles.inspect} line_said=#{LampCap.lines} " \
          "pos=#{$game_player.x},#{$game_player.y} party=[#{lamp_party}] hp=#{$player.party.map(&:hp).inspect} frames=#{f}")
      # --- back up: the first step off the landing starts the finale
      lamp_goto(106, 4, 8, 2)
      $game_player.move_right
      f = lamp_run(400, 20) { !$game_player.moving? && ($game_system.map_interpreter.running? || PrismfallMaps.flags[:il1_boat]) }
      log("gallery touch: boat flag=#{PrismfallMaps.flags[:il1_boat].inspect} running=#{$game_system.map_interpreter.running?}")
      lamp_fail("the gallery step did not start the finale") if !PrismfallMaps.flags[:il1_boat]
      f = lamp_run(9000) { $game_variables[125] >= 13 && $game_map.map_id == 182 && lamp_idle? && $game_screen.tone.red > -100 }
      restored = $player.party.map { |p| p.personalID } == own
      log("RESULT act end: CH5_STEP=#{$game_variables[125]} V119=#{$game_variables[119]} ACT=#{$game_variables[101]} CHAPTER=#{$game_variables[102]} " \
          "S162=#{$game_switches[162]} map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} name=#{$player.name} " \
          "charset=#{$game_player.character_name} opacity=#{$game_player.opacity} party_restored=#{restored} party=[#{lamp_party}] " \
          "hp=#{$player.party.map(&:hp).inspect} interlude=#{Prismfall::Interlude.active?} tone=#{$game_screen.tone.red.round} " \
          "frames=#{f} secs=#{(System.uptime - t0).round(1)}")
      lamp_run(60, 60) { true }
      self.auto = false
      stop
      log("done")
    end
  end
  module Input
    class << self
      alias lamp_trigger? trigger? unless method_defined?(:lamp_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return lamp_trigger?(button)
      end
    end
  end
  class Battle
    alias lamp_pbCommandPhase pbCommandPhase unless method_defined?(:lamp_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        DemoRun.stop if ENV["LAMP_SHOTS"] == "memory"          # the memory flash is on film by now
        foes = @battlers.compact.select(&:opposes?).map { |b| "#{b.species}/L#{b.level}" }
        mine = @battlers.compact.reject(&:opposes?).map { |b| "#{b.pokemon.name}/L#{b.level}" }
        # Kestrel's "Hold. Hold it." (017's own pbCommandPhase alias runs before this one and has said it by now)
        LampCap.lines += 1 if PrismfallLamplight.instance_variable_get(:@line).nil?
        LampCap.battles << [foes, mine, "balls_off=#{@disablePokeBalls}", "can_lose=#{@canLose}", "run=#{@canRun}",
                            "field=#{(respond_to?(:prismfall_field) ? prismfall_field : nil).inspect}"].flatten
        DemoRun.log("battle: #{LampCap.battles.last.inspect}")
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = (LampCap.battles.length == 1) ? 2 : 1
        return
      end
      lamp_pbCommandPhase
    end
  end
end
