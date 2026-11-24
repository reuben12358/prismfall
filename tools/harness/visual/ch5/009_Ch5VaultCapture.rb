#===============================================================================
# Ch5 the Spire Shatter (map 952) in the real engine, dev tool (Wave 0 rescue check, 2026-11-23).
# Plays the vault autorun at CH5_STEP 8: the Mourner's acting sheets (act_ch5_mourner_reach / _burn), the
# Movies/pf_ch5_spire_shatter(.ogv | _safe.ogv) cut (VAULT_SAFE=1 = photosensitive), the Overcharged
# Electivire (auto-won), then CH5_STEP 9. Then the 3 a.m. return: CH5_STEP 11 on 608, the service door
# into the vault, Larch at the cradle (CH5_STEP 12). RESULT lines in demo.log.
#   bash tools/harness/visual/intro/run_intro.sh --capture ../ch5/009_Ch5VaultCapture.rb --plan vault
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
      log("movie file: #{Prismfall::Cutscene.movie_file('pf_ch5_spire_shatter').inspect} play_movie=#{Graphics.respond_to?(:play_movie)}")
      self.every = (ENV["VAULT_EVERY"] || "15").to_i    # every 3rd frame filled the disk (2.4 GB)
      record("ch5_vault")
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
      log("RESULT shatter: CH5_STEP=#{$game_variables[125]} S113=#{$game_switches[113]} battles=#{VaultCap.battles.inspect} " \
          "mourner_gone=#{$game_map.events.values.none? { |e| e.name == 'Mourner' && !e.instance_variable_get(:@erased) && e.character_name != '' }} " \
          "frames=#{f} secs=#{(System.uptime - t0).round(1)}")
      # the 3 a.m. return through 608's service door
      $game_variables[125] = 11
      $game_temp.player_new_map_id = 608; $game_temp.player_new_x = 48; $game_temp.player_new_y = 5
      $game_temp.player_new_direction = 8; $game_temp.player_transferring = true
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > 400 || ($game_map.map_id == 608 && f > 60)
      end
      f = 0
      loop do                                    # let 608's Aftermath autorun finish first
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > 2500 || (!$game_system.map_interpreter.running? && f > 30)
      end
      ev = $game_map.events.values.find { |e| e.name == "Service door" }
      log("door event: #{ev&.id} page list #{ev&.list&.length} player #{$game_player.x},#{$game_player.y} dir #{$game_player.direction}")
      # the auto USE presses usually open 608's door on their own while waiting; only force it if still on 608
      $game_system.map_interpreter.setup(ev.list, ev.id) if ev && $game_map.map_id == 608
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > 1500 || ($game_map.map_id == 952 && !$game_system.map_interpreter.running? && f > 60)
      end
      log("RESULT door: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > 600 || (!$game_system.map_interpreter.running? && f > 30)
      end
      cr = $game_map.events.values.find { |e| e.name == "Cradle" }
      $game_system.map_interpreter.setup(cr.list, cr.id) if cr
      log("cradle event: #{cr&.id} page list #{cr&.list&.length}")
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > 2500 || ($game_variables[125] >= 12 && !$game_system.map_interpreter.running?)
      end
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
