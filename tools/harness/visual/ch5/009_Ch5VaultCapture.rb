#===============================================================================
# Ch5 the Spire Shatter (map 952) in the real engine, dev tool (Wave 0 rescue check, 2026-11-23; the
# in-engine scene, 2026-11-25).
# Plays the vault autorun at CH5_STEP 8: pfm_cutscene(:SH1) = the in-engine Shatter scene (Cutscenes 016 /
# 017_AdvancedAnimations.rb: the two at the cradle, the Splitter, the Shatter, the smoking hand, the
# Mourner's exit, the Electivire; VAULT_SAFE=1 = photosensitive; its boxes wait for USE, which the plan
# presses), the Overcharged Electivire (auto-won), then CH5_STEP 9. Then the 3 a.m. return: CH5_STEP 11 on
# 608, the service door into the vault, Interlude I's "Larch (3 a.m.)" autorun (CH5_STEP 12).
# RESULT lines in demo.log: the scene log, where the player was put back, the tone, audio tags with no file.
#   bash tools/harness/visual/intro/run_intro.sh --capture "$PWD/tools/harness/visual/ch5/009_Ch5VaultCapture.rb" --plan vault
#   VAULT_NOREC=1  no frames (RESULT lines only)      VAULT_EVERY=30  capture every Nth frame (0.6 MB each)
#   VAULT_FULL=1  play Gemini's full cut (with the Lowlight cutaway) instead of the script's version
#   VAULT_NOSCENE=1  make the scene unavailable: the event's text fallback must carry the beat
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("vault")
  module VaultCap
    @battles = []
    class << self; attr_accessor :battles; end
  end
  class << DemoRun
    def vault_settle(limit)
      frames = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        frames += 1
        break if frames > limit
        yield(frames) if block_given? && yield(frames) == :stop
      end
      return frames
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("vault capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      Prismfall::Cutscene.photosensitive = (ENV["VAULT_SAFE"] == "1") if defined?(Prismfall::Cutscene)
      $player.party = [DemoRun.mon(:SWAMPERT, 30, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT])]
      $game_variables[125] = 8
      $game_map.setup(952)
      $game_player.moveto(12, 16); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      if ENV["VAULT_FULL"] == "1"
        Prismfall::Cutscene.send(:remove_const, :SH1_LOWLIGHT_CUTAWAY)
        Prismfall::Cutscene.const_set(:SH1_LOWLIGHT_CUTAWAY, true)
      end
      Prismfall::Cutscene::SCENES.delete(:CH5_DC) if ENV["VAULT_NOSCENE"] == "1"
      tone0 = $game_screen.tone
      log("scene CH5_DC: #{Prismfall::Cutscene.scene_status(:CH5_DC).inspect} photosensitive=#{Prismfall::Cutscene.photosensitive?} " \
          "tone before #{[tone0.red, tone0.green, tone0.blue, tone0.gray].inspect}")
      self.every = (ENV["VAULT_EVERY"] || "30").to_i    # every 3rd frame filled the disk (2.4 GB)
      record("ch5_vault") if ENV["VAULT_NOREC"] != "1"     # VAULT_NOREC=1: RESULT lines only, no frames
      self.auto = true
      t0 = System.uptime
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > 9000
        break if $game_variables[125] >= 9 && !$game_system.map_interpreter.running? && f > 200
      end
      Prismfall::Cutscene.scene_log.each { |l| log("scene log: #{l}") }
      cr0 = $game_map.events.values.find { |e| e.name == "Cradle" }
      tone1 = $game_screen.tone
      log("RESULT scene: map=#{$game_map.map_id} player=#{$game_player.x},#{$game_player.y} dir=#{$game_player.direction} " \
          "transparent=#{$game_player.transparent} tone=#{[tone1.red, tone1.green, tone1.blue, tone1.gray].inspect} " \
          "cradle_tile=#{cr0&.tile_id} bgm=#{$game_system.playing_bgm&.name.inspect} " \
          "no_audio_file=#{Prismfall::Cutscene.missing_audio.inspect}")
      log("RESULT shatter: CH5_STEP=#{$game_variables[125]} S113=#{$game_switches[113]} battles=#{VaultCap.battles.inspect} " \
          "mourner_gone=#{$game_map.events.values.none? { |e| e.name == 'Mourner' && !e.instance_variable_get(:@erased) && e.character_name != '' }} " \
          "frames=#{f} secs=#{(System.uptime - t0).round(1)}")
      # the 3 a.m. return: CH5_STEP 11 on 608, the service door (the plan's USE presses open it), the vault, where
      # Interlude I's "Larch (3 a.m.)" autorun (mapgen/layouts/story_interlude1.py) plays and sets CH5_STEP 12.
      # Stop there: 182's "Lamplight" autorun would start the Interlude proper.
      $game_variables[125] = 11
      $game_temp.player_new_map_id = 608; $game_temp.player_new_x = 48; $game_temp.player_new_y = 5
      $game_temp.player_new_direction = 8; $game_temp.player_transferring = true
      trail = []
      forced = false
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        trail << $game_map.map_id if trail.last != $game_map.map_id
        break if f > 6000 || $game_variables[125] >= 12
        next if forced || f < 900 || $game_map.map_id != 608 || $game_system.map_interpreter.running?
        ev = $game_map.events.values.find { |e| e.name == "Service door" }     # the presses didn't open it: force it
        $game_system.map_interpreter.setup(ev.list, ev.id) if ev
        forced = true
      end
      log("RESULT return: maps=#{trail.inspect} door_forced=#{forced} frames=#{f} map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      self.auto = false
      stop
      log("RESULT larch: CH5_STEP=#{$game_variables[125]}")
      log("done")
    end
  end
  module Input
    class << self
      alias vault_trigger? trigger? unless method_defined?(:vault_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return vault_trigger?(button)
      end
    end
  end
  class Battle
    alias vault_pbCommandPhase pbCommandPhase unless method_defined?(:vault_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        DemoRun.log("battle: #{@battlers.compact.select(&:opposes?).map { |b| b.pokemon.name }.inspect}")
        VaultCap.battles << @battlers.compact.select(&:opposes?).map { |b| b.species }
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      vault_pbCommandPhase
    end
  end
end
