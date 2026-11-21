#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Trainer speech capture: one short
# trainer battle per case (up to 6 turns); from the moment the foe's Z-move is
# chosen, every 3rd frame is dumped to Captures/sp_<case>/, and the battle ends
# at the next command phase after the line. Captures/speech/speech.tsv logs the
# dumped frame of every trainer line (:prismfall_trainer_speech).
#   DEMO_PLAN=speech
#   SP_CASES="celestine"            the real data: Celestine's Mimikyu @ Mimikium Z
#            "ebdx_demo"            EBDX's slide-in path: a stock trainer type that has a front sprite
#                                   (Beauty "Demo"), given a demo line by this capture plugin only
#===============================================================================
module SpeechCapture
  module_function

  def cases
    (ENV["SP_CASES"] || "celestine").split(",")
  end

  def mimikyu
    DemoRun.mon(:MIMIKYU, 78, [:PLAYROUGH, :SHADOWCLAW, :SHADOWSNEAK, :SWORDSDANCE], :MIMIKIUMZ)
  end

  def run_all
    Dir.mkdir("Captures/speech") if !Dir.exist?("Captures/speech")
    @tsv = "Captures/speech/speech.tsv"
    File.write(@tsv, "case\tshot\tframe\tevent\ttrainer\tline\n")
    cases.each do |c|
      @current = c
      case c
      when "celestine" then t = NPCTrainer.new("Celestine", :LEADER_CELESTINE)
      when "ebdx_demo"
        t = NPCTrainer.new("Demo", :BEAUTY)
        PrismfallSpeech::LINES[[:BEAUTY, "Demo"]] = { :zmove => "(capture demo) EBDX slides the speaker in for her line." }
      else next
      end
      t.party = [mimikyu]
      t.items = [:MEGARING]
      DemoRun.every = 100000
      party = [DemoRun.mon(:SNORLAX, 80, [:BODYSLAM, :REST], :LEFTOVERS)]
      DemoRun.battle("sp_#{c}", party, :turns => 6) do
        $game_temp.clear_battle_rules
        setBattleRule("field", :FAIRY_TALE)
        setBattleRule("canLose")
        TrainerBattle.start(t)
      end
      DemoRun.every = 100000
      DemoRun.log("speech #{c}: done")
    end
  end

  def logged(event, trainer, lines)
    shots = DemoRun.instance_variable_get(:@shots)
    File.open(@tsv, "a") { |f| f.puts([@current, shots, DemoRun.frame, event, trainer, lines.join(" / ")].join("\t")) }
  end
end

if ENV["DEMO_PLAN"].to_s == "speech"
  EventHandlers.add(:prismfall_zmove_chosen, :speech_capture,
    proc { |battle, idx, _move| DemoRun.every = 3 if idx.odd? })
  EventHandlers.add(:prismfall_trainer_speech, :speech_capture,
    proc { |battle, b, event, lines|
      t = battle.opponent[battle.pbGetOwnerIndexFromBattlerIndex(b.index)]
      SpeechCapture.logged(event, t.name, lines)
      DemoRun.turn_limit = battle.turnCount + 1     # finish this turn, then end the battle
    })

  class << DemoRun
    alias sp_orig_run run unless method_defined?(:sp_orig_run)
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("speech capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      $scene.createSpritesets
      30.times { Graphics.update; $scene.miniupdate }
      $player.name = "Tester"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:CHARMANDER) rescue nil
      $player.badges = Array.new(18) { true }
      Prismfall::LevelCap.unlock_finale! rescue nil
      self.every = 100000
      SpeechCapture.run_all
      log("done")
    end
  end
end
