#===============================================================================
# Audio v4.3 wiring check in the real engine (dev tool, no frames captured). Logs what the engine is asked to play:
#   bash tools/harness/visual/intro/run_intro.sh --capture "$PWD/tools/harness/visual/audio/008_AudioCheck.rb" --plan audiochk
# Needs the staged audio in the capture copy first: python3 -I audio/install_audio.py /home/claude/run_intro/game --force
# RESULT lines in demo.log: map BGM / BGS after real transfers (town -> interior -> rainy town -> Poke Center),
# trainer intro / battle / victory music, the badge jingle, voice blips on a tagged line, the stock stand-in.
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("audiochk")
  module AudioChk
    @calls = []
    @press_at = nil
    class << self
      attr_accessor :calls, :press_at
      def note(kind, file); @calls << [kind, File.basename(file.to_s).sub(/\.\w+\z/, "")]; end
      def take; c = @calls; @calls = []; return c; end
      def brief(calls, kinds)
        return calls.select { |c| kinds.include?(c[0]) }.map { |c| "#{c[0]}:#{c[1]}" }.chunk_while { |a, b| a == b }.map { |g| (g.length > 1) ? "#{g[0]} x#{g.length}" : g[0] }.join(", ")
      end
      def go(map, x = 8, y = 8)
        $game_temp.player_transferring = true
        $game_temp.player_new_map_id = map
        $game_temp.player_new_x = x
        $game_temp.player_new_y = y
        $game_temp.player_new_direction = 2
        $scene.transfer_player
        5.times { Graphics.update }
      end
      def state
        m = $game_system.playing_bgm
        s = $game_system.playing_bgs
        raw = $game_map.instance_variable_get(:@map)
        return "map #{$game_map.map_id} bgm=#{m ? m.name : '-'} bgs=#{s ? "#{s.name}@#{s.volume}" : '-'} (map file says bgm=#{raw.bgm.name.inspect} bgs=#{raw.bgs.name.inspect})"
      end
    end
  end
  module Audio
    class << self
      %w[bgm_play bgs_play me_play se_play].each do |m|
        alias_method "audiochk_#{m}", m unless method_defined?("audiochk_#{m}")
        define_method(m) do |file, *rest|
          AudioChk.note(m.sub("_play", "").to_sym, file)
          send("audiochk_#{m}", file, *rest)
        end
      end
      %w[bgm_fade bgs_fade bgs_stop].each do |m|
        alias_method "audiochk_#{m}", m unless method_defined?("audiochk_#{m}")
        define_method(m) do |*args|
          AudioChk.note(m.to_sym, "")
          send("audiochk_#{m}", *args)
        end
      end
    end
  end
  module Input
    class << self
      alias audiochk_trigger? trigger? unless method_defined?(:audiochk_trigger?)
      def trigger?(button)
        if button == Input::USE && AudioChk.press_at && System.uptime >= AudioChk.press_at
          AudioChk.press_at = System.uptime + 0.6
          return true
        end
        return audiochk_trigger?(button)
      end
    end
  end
  class Battle
    alias audiochk_pbCommandPhase pbCommandPhase unless method_defined?(:audiochk_pbCommandPhase)
    def pbCommandPhase
      30.times { @scene.pbUpdate rescue Graphics.update }
      @decision = 1
    end
  end
  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("audiochk boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 1
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 60, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT])]
      ac = Prismfall::AudioCue
      log("RESULT installed: #{%w[BGM/Town\ -\ Ferrows\ Landing BGS/Saltmere\ Harbor BGM/Battle\ -\ Warden SE/Voice\ -\ Juno ME/Warden\ Badge\ Get].map { |f| "#{f}=#{FileTest.audio_exist?('Audio/' + f)}" }.join(' ')}")
      $scene.disposeSpritesets rescue nil     # the map scene has no spritesets yet at this point
      $scene.createSpritesets
      AudioChk.take
      AudioChk.go(100)
      log("RESULT town: #{AudioChk.state} | #{AudioChk.brief(AudioChk.take, [:bgm, :bgs, :bgm_fade, :bgs_fade, :bgs_stop])}")
      AudioChk.go(104)
      log("RESULT interior (same music, ambience off): #{AudioChk.state} | #{AudioChk.brief(AudioChk.take, [:bgm, :bgs, :bgm_fade, :bgs_fade, :bgs_stop])}")
      AudioChk.go(140)
      log("RESULT Saltmere: #{AudioChk.state} weather=#{$game_screen.weather_type}")
      $game_screen.weather(:Rain, 9, 0)
      PrismfallMaps.sync_weather_bgs
      log("RESULT Saltmere in rain: #{AudioChk.state}")
      $game_screen.weather(:None, 0, 0)
      PrismfallMaps.sync_weather_bgs
      log("RESULT Saltmere, rain over: #{AudioChk.state}")
      AudioChk.take
      AudioChk.go(141)
      log("RESULT Poke Center (stock music kept): #{AudioChk.state} | #{AudioChk.brief(AudioChk.take, [:bgm, :bgs, :bgm_fade, :bgs_fade, :bgs_stop])}")
      AudioChk.go(544)
      log("RESULT cave: #{AudioChk.state}")
      # trainer music
      %i[LEADER_TAMSIN RIVAL_KESTREL HOLLOW_GRUNT_M MERIDIAN_VOSS FESTIVAL_LIN GILDED_AURELIUS ASHKAAR_OFFICER].each do |t|
        b = pbGetTrainerBattleBGMFromType(t)
        log("RESULT type #{t}: battle=#{b.is_a?(String) ? b : b.name} intro=#{GameData::TrainerType.get(t).intro_BGM.inspect}")
      end
      log("RESULT stand-in for a track that is not installed: Victory - Sovereign -> #{ac.installed('Victory - Sovereign').inspect}; Battle - Nope -> #{ac.installed('Battle - Nope').inspect}")
      AudioChk.take
      pbPlayTrainerIntroBGM(:HOLLOW_GRUNT_M)
      log("RESULT grunt eye contact: #{AudioChk.brief(AudioChk.take, [:bgm, :me])}")
      AudioChk.press_at = System.uptime + 1.0
      setBattleRule("canLose")
      won = (TrainerBattle.start(:LEADER_TAMSIN, "Tamsin") rescue "#{$!.class}: #{$!.message}")
      log("RESULT battle vs LEADER_TAMSIN (#{won.inspect}): #{AudioChk.brief(AudioChk.take, [:bgm, :me])}")
      10.times { Graphics.update }
      log("RESULT after the battle: #{AudioChk.state}")
      AudioChk.take
      $player.badges[0] = false
      Prismfall.award_badge(1, false)
      log("RESULT badge jingle: #{AudioChk.brief(AudioChk.take, [:me])}")
      # voice blips: a tagged line, typed at Mid speed
      AudioChk.take
      AudioChk.press_at = System.uptime + 4.0
      pbMessage("\\pf[JUNO,happy]Juno: Testing the voice blips, one letter at a time, all the way to the end.")
      v = AudioChk.take.select { |c| c[0] == :se && c[1].start_with?("Voice") }
      log("RESULT voice blips on Juno's line: #{v.length} x #{v.map { |c| c[1] }.uniq.inspect}")
      AudioChk.press_at = System.uptime + 3.0
      pbMessage("The ferry horn sounds twice. Nobody is speaking on this line.")
      v = AudioChk.take.select { |c| c[0] == :se && c[1].start_with?("Voice") }
      log("RESULT voice blips on narration: #{v.length}")
      $PokemonSystem.pf_voice_blips = 1
      AudioChk.press_at = System.uptime + 3.0
      pbMessage("\\pf[JUNO,happy]Juno: And with Voice Blips off in the options, nothing at all.")
      v = AudioChk.take.select { |c| c[0] == :se && c[1].start_with?("Voice") }
      log("RESULT voice blips with the option off: #{v.length}")
      AudioChk.press_at = nil
      log("done")
    end
  end
end
