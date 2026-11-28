#===============================================================================
# Ch0, the last ferry (map 109, the Dovetail) in the real engine, dev tool (integration audit 2026-11-27: Gemini's
# 109 overhaul re-tiled the deck under story_early's events). Plays the Prologue autorun (the card, the reflection
# choice, the manifest name, difficulty), then the rail twice (Edda, then Voss: PRO_FERRY_DONE), then the gangway
# to Ferrow's Landing (100). Also takes ONE frame of a message box (the Deckhand's line) to check the speech
# windowskin ("speech hgss 1", Gemini's centred skin of 2026-11-26): Captures/ferry_msgbox.bmp.
# RESULT lines in demo.log. No frame sequence is recorded. Switch names come from Data/system_prismfall.txt, in memory.
#   cp maps_out/Data/Map{100,108,109,110}.rxdata maps_out/Data/system_prismfall.txt /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/intro/012_Ch0FerryCapture.rb --plan ferry
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ferry")
  module FerryCap
    @text = ""; @since = 0; @shot = false; @lines = 0
    class << self; attr_accessor :text, :since, :shot, :lines; end
  end

  # the manifest's name entry would wait for typing: name the player instead
  def pbTrainerName(*_args)
    $player.name = "Wren"
    return true
  end

  alias ferry_pbMessageDisplay pbMessageDisplay unless defined?(ferry_pbMessageDisplay)
  def pbMessageDisplay(msgwindow, message, *args, &block)
    FerryCap.text = message.to_s; FerryCap.since = DemoRun.frame; FerryCap.lines += 1
    return ferry_pbMessageDisplay(msgwindow, message, *args, &block)
  end

  module Graphics
    class << self
      alias ferry_update update unless method_defined?(:ferry_update)
      def update
        ferry_update
        if !FerryCap.shot && FerryCap.text.include?("Twenty minutes") && DemoRun.frame - FerryCap.since == 70
          Graphics.screenshot("#{DemoRun::ROOT}/ferry_msgbox.bmp")
          FerryCap.shot = true
          DemoRun.log("msgbox frame taken: skin=#{($game_system.windowskin_name rescue nil).inspect} " \
                      "speech=#{(MessageConfig.pbGetSpeechFrame rescue nil).inspect}")
        end
      end
    end
  end

  class << DemoRun
    def ferry_play(limit)
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > limit
        break if yield(f)
      end
      return f
    end

    def ferry_ev(name); return $game_map.events.values.find { |e| e.name == name }; end
    def busy?; return $game_system.map_interpreter.running? || $game_temp.message_window_showing || $game_player.moving?; end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ferry capture boot ok")
      Graphics.transition(0)
      # as the vault plan: no install prompt (it waits for a key); set the deck up by hand below
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      # switch-conditioned pages need the switch NAMED in System.rxdata (Game_Event#switchIsOn?); the test copy may
      # not have run the installer: name ours in memory only (Data/system_prismfall.txt, as the installer would)
      if defined?(PrismfallMapInstaller) && FileTest.exist?(PrismfallMapInstaller::SYSTEM_FILE)
        named = 0
        PrismfallMapInstaller.system_entries.each do |kind, id, name|
          names = (kind == "S") ? $data_system.switches : $data_system.variables
          next if !names[id].to_s.empty?
          names[id] = name; named += 1
        end
        log("switch / variable names added in memory: #{named}")
      end
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      if $game_map.map_id != 109
        log("start map was #{$game_map.map_id}: setting up 109")
        $game_map.setup(109); $game_player.moveto(7, 6); $game_player.turn_up
        $scene.disposeSpritesets rescue nil
        $scene.createSpritesets
      end
      $game_map.need_refresh = true
      log("start: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      self.auto = true
      # 1. the Prologue autorun
      intro = ferry_ev("Prologue intro")
      f = ferry_play(9000) { |n| n > 120 && $game_self_switches[[109, intro.id, "A"]] && !busy? }
      log("RESULT prologue: done=#{$game_self_switches[[109, intro.id, 'A']]} frames=#{f} name=#{$player.name} " \
          "charset=#{$game_player.character_name} difficulty=#{(Prismfall::Difficulty.current rescue nil).inspect} " \
          "act=#{$game_variables[101]} chapter=#{$game_variables[102]} lines=#{FerryCap.lines} msgbox_shot=#{FerryCap.shot}")
      [1, 2].each do |pid|      # Core 026: the movement sheets each look resolves to (surf-fish: Gemini's seated sheet)
        md = GameData::PlayerMetadata.get(pid) rescue nil
        log("RESULT look #{pid}: " + [:walk, :run, :cycle, :surf, :dive, :fish, :surf_fish].map { |k|
          "#{k}=#{(md.send(:"#{k}_charset") rescue '?')}" }.join(" ")) if md
      end
      # 2. the rail, twice: Edda, then Voss (PRO_FERRY_DONE)
      done_sw = 101
      2.times do |i|
        $game_player.moveto(12, 7); $game_player.turn_up
        f = ferry_play(600) { |n| n > 10 && !busy? }
        $game_player.move_up
        f = ferry_play(12000) { |n| n > 60 && !busy? }
        log("RESULT rail #{i + 1}: frames=#{f} dove_edda=#{pfm?(:dove_edda)} dove_voss=#{pfm?(:dove_voss)} " \
            "PRO_FERRY_DONE=#{$game_switches[done_sw]} pos=#{$game_player.x},#{$game_player.y} lines=#{FerryCap.lines}")
      end
      # 3. the gangway to Ferrow's Landing (the Deckhand walks at random and can stand in the way: step again
      # every second until the deck is left, and say who was in the way)
      $game_player.moveto(9, 14); $game_player.turn_down
      ferry_play(300) { |n| n > 10 && !busy? }
      tries = 0; blockers = []
      gw = ferry_ev("Gangway")
      f = ferry_play(3000) do |n|
        if $game_map.map_id == 109 && !busy? && n % 60 == 1
          if $game_player.x != 9 || $game_player.y != 14
            $game_player.moveto(9, 14); $game_player.turn_down
          end
          who = $game_map.events.values.find { |e| e.x == 9 && e.y == 15 && e.character_name != "" }
          blockers << who.name if who && !blockers.include?(who.name)
          tries += 1
          $game_player.move_down
        end
        $game_map.map_id != 109 && n > 60 && !busy?
      end
      log("RESULT gangway: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} frames=#{f} tries=#{tries} " \
          "blocked_by=#{blockers.inspect} gangway_page=#{(gw.instance_variable_get(:@page) && gw.list.length) rescue '?'} " \
          "last_line=#{FerryCap.text[0, 60].inspect}")
      self.auto = false
      log("done")
    end
  end
  module Input
    class << self
      alias ferry_trigger? trigger? unless method_defined?(:ferry_trigger?)
      def trigger?(button)
        return DemoRun.frame % 40 == 0 if button == Input::USE && DemoRun.auto
        return ferry_trigger?(button)
      end
    end
  end
end
