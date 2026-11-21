#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Full trainer battle opening, player vs Juno (J1):
# Juno's pre-battle line with her face portrait -> EBDX trainer transition with the integrated VS cut-in
# -> "You are challenged by Rival Juno!" -> both send-outs -> command menu.
#   DEMO_PLAN=intro   IC_EVERY=2 (frame step)   IC_PRESS=80 (frames between message presses)
#   IC_PLAYER=A|B     IC_VERSION=10 (J1 Standard)   IC_FIELD=MEADOW
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("intro")
  # Rivals get EBDX's integrated VS cut-in (uses the trainer's own battle sprite; no extra art needed).

  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("intro capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      $scene.createSpritesets
      30.times { Graphics.update; $scene.miniupdate }
      $player.name = (ENV["IC_PLAYER"] == "B") ? "Rae" : "Wren"
      pbChangePlayer((ENV["IC_PLAYER"] == "B") ? 2 : 1)   # the intro's look choice (Prismfall Core 026)
      $PokemonSystem.textspeed = 1
      $PokemonSystem.battlescene = 0
      # the player's battle art: copy the chosen Gemini player onto the player's trainer type for this run
      tt = $player.trainer_type.to_s
      src = (ENV["IC_PLAYER"] == "B") ? "PLAYER_B" : "PLAYER_A"
      ["", "_back"].each do |suf|
        break if tt.start_with?("PLAYER_")              # Prismfall Core 026 already gives the player their art
        s = "Graphics/Trainers/#{src}#{suf}.png"
        File.binwrite("Graphics/Trainers/#{tt}#{suf}.png", File.binread(s)) if File.exist?(s)
      end
      log("player trainer type #{tt} <- #{src}")
      Prismfall.record_starter(:MUDKIP) rescue nil
      self.every = (ENV["IC_EVERY"] || 2).to_i
      party = [DemoRun.mon(:MUDKIP, 15, [:WATERGUN, :MUDSLAP, :ROCKTOMB, :PROTECT]),
               DemoRun.mon(:WOOLOO, 13, [:TACKLE, :DEFENSECURL])]
      # Saltmere promenade green (map 140), stood in front of the real "Juno J1" event with Gemini's JUNO charset
      begin
        $game_map.setup(140)
        ev = $game_map.events.values.find { |e| e.name == "Juno J1" }
        jx, jy = ev ? [ev.x, ev.y] : [37, 53]
        $game_player.moveto(jx, jy + 2); $game_player.turn_up
        if ev
          ev.instance_variable_set(:@character_name, "JUNO"); ev.instance_variable_set(:@direction, 2)
          ev.instance_variable_set(:@opacity, 255); ev.instance_variable_set(:@transparent, false)
        end
        $scene.disposeSpritesets rescue nil
        $scene.createSpritesets
        $game_screen.start_tone_change(Tone.new(0, 0, 0, 0), 0) rescue nil
        log("map 140 at #{jx},#{jy + 2} juno event #{ev ? 'found' : 'MISSING'}")
      rescue => e
        log("map setup failed #{e.class}: #{e.message}")
      end
      DemoRun.battle("intro_#{(ENV['IC_FOE'].to_s.empty? ? 'juno' : ENV['IC_FOE']).downcase}_#{ENV['IC_PLAYER'] || 'A'}", party, :turns => 1) do
        40.times { Graphics.update; $scene.miniupdate }
        # Juno's pre-battle line in the overworld, with her face portrait (SPINE Rev 22)
        # (the real J1 lines from mapgen/layouts/saltmere_rj.py juno_j1)
        if ENV["IC_FOE"] != "DORIAN"
          pbMessage("\\pf[JUNO,happy]Juno: There you are! Tarts delivered! Forty! I ate one. Thirty-nine!")
          pbMessage("\\pf[JUNO,neutral]Juno: Before you go in there... fight me?")
        end
        $game_temp.clear_battle_rules
        if ENV["IC_FOE"] == "DORIAN"
          pbMessage("\\pf[DORIAN,smug]Dorian: Enter, stage left, our brave challenger! The spotlight is yours, darling.")
          $game_temp.clear_battle_rules
          setBattleRule("field", :GRAND_STAGE) rescue nil
          TrainerBattle.start(:LEADER_DORIAN, "Dorian")
        else
          Prismfall.rival_battle(:RIVAL_JUNO, "Juno", 1, can_lose: true, field: (ENV["IC_FIELD"] || "MEADOW").to_sym)
        end
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

  module Input
    class << self
      alias ic_trigger? trigger? unless method_defined?(:ic_trigger?)
      def trigger?(button)
        if button == Input::USE && DemoRun.auto
          return DemoRun.frame % (ENV["IC_PRESS"] || 80).to_i == 0
        end
        return ic_trigger?(button)
      end
    end
  end

  class Battle
    alias ic_pbCommandPhase pbCommandPhase unless method_defined?(:ic_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        DemoRun.log("command phase reached")
        90.times { @scene.pbUpdate rescue Graphics.update }   # hold on the battle with both sides out
        @decision = 3
        return
      end
      ic_pbCommandPhase
    end
  end
end
