#===============================================================================
# The in-engine live-map scenes (Cutscenes 016 registry + 017_AdvancedAnimations.rb) in the real engine,
# dev tool. Starts a new game on a "home" map, plays each scene through pfm_cutscene(id, preview: true)
# (so scenes still staged on a stand-in map play too) and checks the game gets the map, the player, the
# tone back and control returns to the map loop. RESULT lines in demo.log; frames in ch00_scene_<ID>.
#   SCENE_IDS=CH2_PAGEANT,CH8_CALDERA bash tools/harness/visual/intro/run_intro.sh \
#     --capture "$PWD/tools/harness/visual/cutscenes/008_SceneCapture.rb" --plan scenes
#   SCENE_HOME=952,12,16  where the player stands before each scene (map,x,y)
#   SCENE_AUTO=1          timed boxes (AdvancedAnimations.auto_advance) instead of the plan pressing USE
#   SCENE_SAFE=1          photosensitive mode        SCENE_PLAYER=2  the other protagonist
#   SCENE_EVERY=15        capture every Nth frame (BMP, ~0.6 MB each: keep it sparse and delete the frames)
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("scenes")
  class << DemoRun
    def scene_state
      t = $game_screen.tone
      return [$game_map.map_id, $game_player.x, $game_player.y, $game_player.direction, $game_player.transparent,
              [t.red, t.green, t.blue, t.gray], $game_map.display_x, $game_map.display_y]
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("scenes capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer((ENV["SCENE_PLAYER"] || "1").to_i)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      Prismfall::Cutscene.photosensitive = (ENV["SCENE_SAFE"] == "1")
      Prismfall::AdvancedAnimations.auto_advance = (ENV["SCENE_AUTO"] == "1")
      home = (ENV["SCENE_HOME"] || "952,12,16").split(",").map(&:to_i)
      $game_map.setup(home[0])
      $game_player.moveto(home[1], home[2]); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      40.times { Graphics.update; Input.update; $scene.update }
      self.every = (ENV["SCENE_EVERY"] || "15").to_i
      self.auto = true
      ids = (ENV["SCENE_IDS"] || "CH2_PAGEANT").split(",").map { |s| s.strip.to_sym }
      ids.each do |id|
        record("ch00_scene_#{id}")
        before = scene_state
        f0 = DemoRun.frame
        t0 = System.uptime
        ok = pfm_cutscene(id, preview: true)
        secs = (System.uptime - t0).round(1)
        after = scene_state
        30.times { Graphics.update; Input.update; $scene.update }     # control is back with the map loop
        stop
        log("RESULT #{id}: played=#{ok} status=#{Prismfall::Cutscene.scene_status(id).inspect} secs=#{secs} frames=#{DemoRun.frame - f0} " \
            "restored=#{before == after} before=#{before.inspect} after=#{after.inspect} | #{Prismfall::Cutscene.scene_log.last}")
      end
      log("RESULT no_audio_file: #{Prismfall::Cutscene.missing_audio.inspect}")
      self.auto = false
      log("done")
    end
  end
  module Input
    class << self
      alias scenes_trigger? trigger? unless method_defined?(:scenes_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return scenes_trigger?(button)
      end
    end
  end
end
