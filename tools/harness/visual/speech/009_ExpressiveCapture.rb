#===============================================================================
# Expressive conversation (Cutscenes 018) and the Act I -> II transition (END OF ACT I, then Chapter 6's
# card, Cutscenes 020) in the real engine, dev tool. RESULT lines in demo.log.
#   1. On the start map: Juno and Kestrel stand two tiles up from the player and talk to each other (two-speaker
#      stage, a \pfe balloon on two lines, a \pfp stance, a \pfa step back); they should turn to each other
#      (018's auto_face :context). Then the PC speaks and Kestrel answers: nobody turns.
#   2. Map 106's "Lamplight finale" autorun (Interlude I's last scene) with the automatic chapter card ON:
#      the card order is logged (expected: PF_ACT1_END while V102 = 5, then the CH06 card, no "II — IMPRINTS").
#   cp maps_out/Data/Map{106,182}.rxdata maps_out/Data/system_prismfall.txt /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture "$PWD/tools/harness/visual/speech/009_ExpressiveCapture.rb" --plan expr
# Frames (sparse): frames/ch0_expr (the talk), ch0_actend and ch0_ch6card (the two cards). Delete them and the
# same folders in captures_keep/ after looking. EXPR_EVERY = frame stride (default 45).
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("expr")
  module ExprCap
    @press = false
    @cards = []
    class << self; attr_accessor :press, :cards; end
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

    def expr_step(limit, min = 30)
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > limit || (f > min && yield)
      end
      return f
    end

    # Logs every title card and chapter card as it starts, with V102 at that moment, and records a few frames of it.
    def expr_watch_cards
      stride = (ENV["EXPR_EVERY"] || "45").to_i
      Object.send(:alias_method, :expr_pfm_card, :pfm_card)
      Object.send(:define_method, :pfm_card) do |scene, *lines|
        ExprCap.cards << [scene, $game_variables[102]]
        DemoRun.every = stride
        DemoRun.record("ch0_actend") if scene == :PF_ACT1_END
        r = expr_pfm_card(scene, *lines)
        DemoRun.stop
        r
      end
      cc = Prismfall::ChapterCards
      cc.singleton_class.send(:alias_method, :expr_play, :play)
      cc.define_singleton_method(:play) do |id, **opts|
        ExprCap.cards << [cc.resolve_key(id), $game_variables[102]]
        DemoRun.every = stride
        DemoRun.record("ch0_ch#{$game_variables[102]}card")
        r = expr_play(id, **opts)
        DemoRun.stop
        r
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
      Prismfall::ChapterCards.auto = true           # off by default under DEMO_PLAN; on here, as in play
      ex = Prismfall::Expressive
      pf = Prismfall::Portrait
      #--- 1. two characters talking to each other -----------------------------------------------------------
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
      self.every = (ENV["EXPR_EVERY"] || "45").to_i
      record("ch0_expr")
      expr_idle(40)
      ExprCap.press = true
      views = []
      pf.singleton_class.send(:alias_method, :expr_open_real, :open)
      pf.define_singleton_method(:open) { |sp, win = nil, mode = nil| v = expr_open_real(sp, win, mode); views.push(v); v }
      begin
        log("auto_face=#{ex.auto_face.inspect} face_mode=#{ex.face_mode.inspect} start dirs juno=#{juno.direction} kestrel=#{kes.direction} player=#{$game_player.direction}")
        pbMessage("\\pf[JUNO,happy]Juno: Kestrel! You came back to Briarwick. I wasn't sure you would.")
        pbMessage("\\pf[KESTREL,deadpan]\\pfp[crossed]Kestrel: Don't make a fuss. I only stopped by for Larch's report.")
        r2 = [juno.direction, kes.direction, kes.pf_pose_sheet, views.last.side, views.last.listener && views.last.listener.id]
        pbMessage("\\pf[JUNO,sad]\\pfe[question]Juno: You heard what happened at the Spire... didn't you?")
        pbMessage("\\pf[KESTREL,sad]\\pfe[dots]\\pfa[step_back]Kestrel: ...Keep off the ridge tonight. Meridian's watching.")
        r4 = [ex.emotes_shown, kes.pf_visual_ox, kes.pf_visual_oy]
        kes.pf_set_facing(2)                              # Kestrel turns to the PC...
        pbMessage("\\pf[PLAYER,neutral]Wren: I'll be careful.")
        pbMessage("\\pf[KESTREL,neutral]Kestrel: You won't. Nobody is.")
        r6 = [juno.direction, kes.direction, $game_player.direction]
        log("RESULT talk: after line 2 [juno_dir, kestrel_dir, stance, side, listener]=#{r2.inspect} (expect 6, 4) " \
            "line 4 [emotes, ox, oy]=#{r4.inspect} after the PC's line [juno, kestrel, player]=#{r6.inspect} (expect 6, 2, 8) " \
            "views=#{views.map { |v| v.class.name.split('::').last }.uniq.inspect}")
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(12).join("\n  "))
      end
      ExprCap.press = false
      expr_idle(30)
      stop
      log("RESULT after the talk: active=#{ex.active?} poses=#{[juno.pf_pose_sheet, kes.pf_pose_sheet].inspect} " \
          "offsets=#{[kes.pf_visual_ox, kes.pf_visual_oy].inspect} live_portrait=#{pf.current.inspect}")
      #--- 2. the end of Act I on 106 ------------------------------------------------------------------------
      begin
        expr_watch_cards
        Prismfall::ChapterCards.seen.push(:CH05)        # Chapter 5's card belongs to an earlier save state
        $game_variables[102] = 5
        $game_variables[101] = 1
        $game_variables[125] = 12
        $game_variables[119] = 1                          # the interlude is running (the finale's page condition)
        $game_map.setup(106)
        $game_player.moveto(4, 7)
        $game_player.turn_up
        %w[Lamplight\ (lamp\ room) Lamplight\ finale].each do |name|
          ev = $game_map.events.values.find { |e| e.name == name }
          log("event #{name}: #{ev&.id.inspect}")
          $game_self_switches[[106, ev.id, "A"]] = true if ev
        end
        $scene.disposeSpritesets rescue nil
        $scene.createSpritesets
        $game_map.need_refresh = true
        ExprCap.press = true
        t0 = System.uptime
        f = expr_step(9000, 60) { $game_variables[125] >= 13 && $game_map.map_id == 182 && !$game_system.map_interpreter.running? }
        ExprCap.press = false
        log("RESULT act end: cards (id, V102 when it began)=#{ExprCap.cards.inspect} (expect PF_ACT1_END @5, CH06 @6) " \
            "ACT=#{$game_variables[101]} CHAPTER=#{$game_variables[102]} map=#{$game_map.map_id} seen=#{Prismfall::ChapterCards.seen.inspect} " \
            "frames=#{f} secs=#{(System.uptime - t0).round(1)}")
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(12).join("\n  "))
      end
      stop
      log("done")
    end
  end
  module Input
    class << self
      alias expr_trigger? trigger? unless method_defined?(:expr_trigger?)
      def trigger?(button)
        return false if button == Input::USE && Prismfall::ChapterCards.playing?    # let a card play out for the frames
        return DemoRun.frame % 90 == 0 if button == Input::USE && ExprCap.press
        return expr_trigger?(button)
      end
    end
  end
end
