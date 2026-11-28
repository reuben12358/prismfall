#===============================================================================
# Ch8 Trials in the real engine, dev tool (plugins/Prismfall Trials/121_Quests_Cindervault.rb,
# mapgen/trial_overlay.py 240 / 247). Starts the placed quests through the BUILT map events (each event
# is started where it stands; its page is the one Essentials picks, its script calls pf_trial_talk):
#   240 "Adequate Swords Owner" (offer) -> "Kessa (Excellent Swords)" (the blade-test battle)
#   240 "Legate Varra Kosk" (Seven Bouts: seven auto-won battles, no bag)
#   247 "Tribune Halden" hidden until the Trial opens -> "Oath-Scribe" (the Honest Court) -> "Herald Pyke"
#       (the Trial of Truth: the truth, then the oath duel)
#   248 "Recruit Tamm" (Afraid of Heights: the offer and the first spar)
#   240 "Adequate Swords Owner" (home: Metal Coat) and its sign (now ready)
# Battles are auto-won after 60 frames; choices come from a queue (0-based, per talk). RESULT lines in demo.log
# carry the quest states, steps, flags, items and every battle's opponent and field.
#   DEMO_PLAN=trials8 bash tools/harness/visual/intro/run_intro.sh --capture <abs path> --plan trials8
# TRIALS8_SHOTS=1 records every 120th frame of the first two talks (Captures/ch8_trials; run_intro moves it to
# frames/ and keeps a second copy in captures_keep/: delete both after looking).
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("trials8")
  module Trials8Cap
    @queue = []; @battles = []
    class << self; attr_accessor :queue, :battles; end
  end
  class << DemoRun
    def t8_goto(mid, x, y)
      $game_map.setup(mid)
      $game_player.moveto(x, y); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      30.times { Graphics.update; Input.update; $scene.update }
    end

    def t8_event(name)
      $game_map.events.values.find { |e| e.name == name }
    end

    # Start a built map event as if the player pressed USE on it; run until its interpreter is done.
    def t8_talk(name, choices = [])
      ev = t8_event(name)
      if !ev
        log("RESULT talk #{name}: NO SUCH EVENT on #{$game_map.map_id}")
        return
      end
      Trials8Cap.queue = choices.dup
      $game_player.moveto(ev.x, ev.y + 1) rescue nil
      $game_player.turn_up
      $game_map.need_refresh = true
      5.times { Graphics.update; Input.update; $scene.update }
      ev.start
      frames = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        frames += 1
        break if frames > 12000
        break if frames > 20 && !$game_system.map_interpreter.running? && !ev.starting && !$game_temp.in_battle
      end
      log("RESULT talk #{name} on #{$game_map.map_id}: frames=#{frames} unused_choices=#{Trials8Cap.queue.length}")
    end

    def t8_state(id)
      tr = Prismfall::Trials
      "#{id} state=#{tr.state(id).inspect} step=#{(tr.active?(id) ? tr.step(id) : nil).inspect} outcome=#{tr.outcome(id).inspect}"
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("trials8 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 45, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 45, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      $player.badges = Array.new(18) { |i| i < 6 }
      $game_switches[120] = true; $game_switches[121] = true
      $game_variables[129] = 10; $game_variables[110] = 0
      tr = Prismfall::Trials
      tr.store[:points][:ASHKAAR] = 8          # Ashkaar rank 3 (the Trial of Truth is a rank-3 writ; Afraid of Heights rank 2)
      t8_goto(240, 20, 30)
      self.every = 120
      record("ch8_trials") if ENV["TRIALS8_SHOTS"] == "1"
      self.auto = true
      log("RESULT start: badges=#{Prismfall.badge_count rescue '?'} ashkaar_rank=#{tr.rank(:ASHKAAR)} S120=#{$game_switches[120]} V129=#{$game_variables[129]} #{t8_state(:AS_ADEQUATE_SWORDS)} #{t8_state(:AS_SEVEN_BOUTS)} #{t8_state(:AS_TRIAL_OF_TRUTH)}")
      # --- 240: Adequate Swords, offer and the blade-test --------------------------------------------
      t8_talk("Adequate Swords Owner", [0])
      log("RESULT after owner: #{t8_state(:AS_ADEQUATE_SWORDS)}")
      t8_talk("Kessa (Excellent Swords)")
      stop
      log("RESULT after Kessa: #{t8_state(:AS_ADEQUATE_SWORDS)} battles=#{Trials8Cap.battles.inspect}")
      # --- 240: Seven Bouts ---------------------------------------------------------------------------
      Trials8Cap.battles.clear
      t8_talk("Legate Varra Kosk", [0])
      log("RESULT after Kosk: #{t8_state(:AS_SEVEN_BOUTS)} charcoal=#{$bag.has?(:CHARCOAL)} firestone=#{$bag.has?(:FIRESTONE)} " \
          "bouts=#{Trials8Cap.battles.length} battles=#{Trials8Cap.battles.inspect}")
      # --- 247: the Honest Court, then the Trial of Truth ---------------------------------------------
      t8_goto(247, 16, 19)
      hal = t8_event("Tribune Halden")
      log("RESULT 247 before the Trial: Halden shown=#{hal && hal.character_name.to_s != ''} page_char=#{hal&.character_name.inspect}")
      t8_talk("Oath-Scribe", [1])
      log("RESULT after the court: #{t8_state(:AS_ADEQUATE_SWORDS)} verdict=#{tr.flag(:AS_ADEQUATE_SWORDS, :verdict).inspect}")
      Trials8Cap.battles.clear
      t8_talk("Herald Pyke", [0, 0])
      hal = t8_event("Tribune Halden")
      log("RESULT after Pyke: #{t8_state(:AS_TRIAL_OF_TRUTH)} flameorb=#{$bag.has?(:FLAMEORB)} battles=#{Trials8Cap.battles.inspect} " \
          "Halden shown now=#{hal && hal.character_name.to_s != ''}")
      # --- 248: Afraid of Heights (the offer runs the first spar) ----------------------------------------
      t8_goto(248, 12, 20)
      Trials8Cap.battles.clear
      t8_talk("Recruit Tamm", [0])
      log("RESULT after Tamm: #{t8_state(:AS_AFRAID_OF_HEIGHTS)} spars=#{tr.count(:AS_AFRAID_OF_HEIGHTS, :spars)} battles=#{Trials8Cap.battles.inspect}")
      # --- 240: home ------------------------------------------------------------------------------------
      t8_goto(240, 20, 30)
      t8_talk("Adequate Swords Owner")
      log("RESULT after home: #{t8_state(:AS_ADEQUATE_SWORDS)} metalcoat=#{$bag.has?(:METALCOAT)} sign_ready=#{pf_trial_ready?(:ADEQUATE_SIGN)} " \
          "ashkaar_points=#{tr.points(:ASHKAAR)}")
      self.auto = false
      stop
      log("done")
    end
  end
  module Input
    class << self
      alias t8_trigger? trigger? unless method_defined?(:t8_trigger?)
      def trigger?(button)
        # only to page messages: a USE press with no message up would start the event in front of the player again
        if button == Input::USE && DemoRun.auto
          return DemoRun.frame % 45 == 0 && ($game_temp.message_window_showing || $game_temp.in_battle)
        end
        return t8_trigger?(button)
      end
    end
  end
  alias t8_pbShowCommands pbShowCommands unless defined?(t8_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = Trials8Cap.queue.shift || 0
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return t8_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias t8_pbCommandPhase pbCommandPhase unless method_defined?(:t8_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        f = (field_effect rescue nil)
        Trials8Cap.battles << "#{names.join('+')}@#{f.inspect}#{@sideSizes[1] > 1 ? '(double)' : ''}"
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      t8_pbCommandPhase
    end
  end
end
