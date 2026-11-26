#===============================================================================
# Expressive conversation (Cutscenes 018) and chapter card (Cutscenes 020) in the real engine, dev tool.
# Stands Juno and Kestrel in front of the player on whatever map a new game starts on, plays a four-line
# exchange through pbMessage (two-speaker stage, one \pfe balloon each for two lines, a \pfp stance, a
# \pfa step back), then chapter 3's card in full, then lets a map event set V102 = 4 (the automatic card,
# skipped with USE). RESULT lines in demo.log.
#   bash tools/harness/visual/intro/run_intro.sh --capture "$PWD/tools/harness/visual/speech/009_ExpressiveCapture.rb" --plan expr
# Frames: /home/claude/run_intro/frames/ch0_expr (sparse; delete them and captures_keep/ch0_expr after looking).
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("expr")
  module ExprCap
    @press = false
    class << self; attr_accessor :press; end
  end
  class << DemoRun
    def expr_event(id, name, charset, x, y, dir = 2)
      ev = RPG::Event.new(x, y)
      ev.id = id
      ev.name = name
      ev.pages[0].graphic.character_name = charset
      ev.pages[0].graphic.direction = dir
      $game_map.events[id] = Game_Event.new($game_map.map_id, ev, $game_map)
    end

    def expr_idle(frames)
      frames.times do
        Graphics.update; Input.update
        $scene.update
      end
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("expr capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      # the base project's start map has an autorun (pbChangePlayer + pbTrainerName, the name entry screen) that would
      # wait forever for typing: drop it before the first full update
      $game_map.events.each_value { |e| e.erase if [3, 4].include?(e.trigger) }
      $game_system.map_interpreter.clear rescue nil
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      Prismfall::ChapterCards.auto = true           # off by default under DEMO_PLAN
      px = $game_player.x
      py = $game_player.y
      $game_player.turn_up
      expr_event(901, "Juno (test)", "JUNO", px - 1, py - 2)
      expr_event(902, "Kestrel K0", "KESTREL", px + 1, py - 2)
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      juno = $game_map.events[901]
      kes = $game_map.events[902]
      self.every = (ENV["EXPR_EVERY"] || "30").to_i
      record("ch0_expr")
      expr_idle(40)
      ExprCap.press = true
      ex = Prismfall::Expressive
      pf = Prismfall::Portrait
      views = []
      pf.singleton_class.send(:alias_method, :expr_open_real, :open)
      pf.define_singleton_method(:open) { |sp, win = nil, mode = nil| v = expr_open_real(sp, win, mode); views.push(v); v }
      begin
        pbMessage("\\pf[JUNO,happy]Juno: Kestrel! You came back to Briarwick. I wasn't sure you would.")
        r1 = [juno.pf_pose_sheet, juno.pf_pose_index]
        pbMessage("\\pf[KESTREL,deadpan]\\pfp[crossed]Kestrel: Don't make a fuss. I only stopped by for Larch's report.")
        r2 = [kes.pf_pose_sheet, kes.pf_pose_index, views.last.side, views.last.listener && views.last.listener.id]
        pbMessage("\\pf[JUNO,sad]\\pfe[question]Juno: You heard what happened at the Spire... didn't you?")
        r3 = [ex.emotes_shown, views.last.entry, views.last.side]
        pbMessage("\\pf[KESTREL,sad]\\pfe[dots]\\pfa[step_back]Kestrel: ...Keep off the ridge tonight. Meridian's watching.")
        r4 = [ex.emotes_shown, kes.pf_visual_ox, kes.pf_visual_oy, views.last.class.name]
        log("RESULT expressive: juno_pose=#{r1.inspect} kestrel=#{r2.inspect} line3=#{r3.inspect} line4=#{r4.inspect} " \
            "views=#{views.map { |v| v.class.name.split('::').last }.inspect}")
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(12).join("\n  "))
      end
      ExprCap.press = false
      expr_idle(30)
      log("RESULT after the event: active=#{ex.active?} juno_pose=#{juno.pf_pose_sheet.inspect} kestrel_pose=#{kes.pf_pose_sheet.inspect} " \
          "offsets=#{[kes.pf_visual_ox, kes.pf_visual_oy].inspect} live_portrait=#{pf.current.inspect}")
      # chapter card, in full
      t0 = System.uptime
      begin
        shown = pf_chapter_card(3, skippable: false)
        again = pf_chapter_card(3)
        log("RESULT card: shown=#{shown} again=#{again} secs=#{(System.uptime - t0).round(1)} seen=#{Prismfall::ChapterCards.seen.inspect}")
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(12).join("\n  "))
      end
      # the automatic card: a map event sets V102
      ExprCap.press = true
      list = [RPG::EventCommand.new(355, 0, ["$game_variables[102] = 4"]), RPG::EventCommand.new(0, 0, [])]
      $game_system.map_interpreter.setup(list, 0)
      t0 = System.uptime
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > 900 || (Prismfall::ChapterCards.seen.include?(:CH04) && !$game_system.map_interpreter.running?)
      end
      ExprCap.press = false
      log("RESULT auto card: V102=#{$game_variables[102]} seen=#{Prismfall::ChapterCards.seen.inspect} secs=#{(System.uptime - t0).round(1)} (skipped with USE)")
      expr_idle(20)
      stop
      log("done")
    end
  end
  module Input
    class << self
      alias expr_trigger? trigger? unless method_defined?(:expr_trigger?)
      def trigger?(button)
        return DemoRun.frame % 120 == 0 if button == Input::USE && ExprCap.press
        return expr_trigger?(button)
      end
    end
  end
end
