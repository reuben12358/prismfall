#===============================================================================
# Real-engine smoke test for the Ch15-21 engine hooks (dev tool; records NO frames).
#   bash tools/harness/visual/intro/run_intro.sh --capture <abs path to this file> --plan tap_hooks
# On the built Steamline (925) it checks the things the headless harness can only fake:
#   the timed prompt's own window loop (times out as the default), the Interlude charset swap on the real
#   Game_Player, pf_echo_follow moving real Game_Events behind real player steps, the lamp board and letterbox
#   as real sprites, the Hush mute through Game_System, the white vision's screen tone.
# RESULT lines go to demo.log (run_intro prints them).
#===============================================================================
if ENV["DEMO_PLAN"].to_s == "tap_hooks"
  class << DemoRun
    def spin(frames)
      frames.times { Graphics.update; Input.update; $scene.update }
    end

    def step_player(dir)
      case dir
      when 6 then $game_player.move_right
      when 4 then $game_player.move_left
      when 2 then $game_player.move_down
      when 8 then $game_player.move_up
      end
      spin(2)
      60.times { break if !$game_player.moving?; spin(1) }
      spin(12)       # the followers' own step
    end

    def result(name)
      v = yield
      log("RESULT #{name}: #{v.inspect}")
    rescue Exception => e
      log("RESULT #{name}: EXCEPTION #{e.class}: #{e.message} @ #{(e.backtrace || []).first}")
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("tap hooks smoke boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $player.party = [DemoRun.mon(:SWAMPERT, 60, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT])]
      $game_system.encounter_disabled = true
      $game_map.setup(925)
      # a straight run of 7 walkable tiles, anywhere on the map
      run_at = nil
      (2...($game_map.height - 2)).each do |y|
        (2...($game_map.width - 9)).each do |x|
          next if !(0..6).all? { |i| $game_map.passable?(x + i, y, 6) && $game_map.passable?(x + i, y, 4) }
          next if $game_map.events.values.any? { |e| e.y == y && e.x >= x && e.x <= x + 7 }
          run_at = [x, y]
          break
        end
        break if run_at
      end
      result("925 walkable run") { run_at }
      $game_player.moveto(*(run_at || [5, 5]))
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      spin(20)

      #--- pf_echo_follow on real events ---------------------------------------
      evs = $game_map.events.values.sort_by(&:id).first(3)
      start = [$game_player.x, $game_player.y]
      result("convoy start (#{evs.length} events)") { pf_echo_follow(:convoy, evs.map(&:id)) }
      4.times { step_player(6) }
      want = [3, 2, 1].map { |i| [start[0] + i, start[1]] }
      result("convoy on the footprints after 4 steps") { [evs.map { |e| [e.x, e.y] } == want, evs.map { |e| [e.x, e.y] }, want, [$game_player.x, $game_player.y]] }
      result("convoy stop") { pf_echo_follow(:stop) }
      result("crypt echo record") { pf_echo_follow(:record, max: 12, var: 370) }
      2.times { step_player(6) }
      result("recorded 2, V370") { [pf_echo_follow(:length), $game_variables[370]] }
      result("replay walks the echo to the player's tile") {
        n = pf_echo_follow(:replay, evs[0].id)
        [n, [evs[0].x, evs[0].y] == [$game_player.x, $game_player.y]]
      }
      pf_echo_follow(:clear, evs[0].id)

      #--- the Interlude swap on the real Game_Player ----------------------------
      own = $game_player.character_name
      result("interlude 4 start") { [pf_interlude_start(4), $game_variables[119], $player.name, $player.party.map(&:species)] }
      spin(5)
      result("Wenlow's charset on the player") { [$game_player.character_name, Prismfall::Interlude.charset] }
      result("interlude end restores the look") { pf_interlude_end; spin(5); [$game_player.character_name == own, $player.name, $player.party.map(&:species), $game_variables[119]] }
      pf_interlude_start(5)
      spin(5)
      result("Valen: charset, walk speed, can't run") { [$game_player.character_name, $game_player.move_speed, $game_player.can_run?] }
      pf_interlude_end
      spin(5)

      #--- the timed prompt's own window loop: nobody presses anything ----------
      t0 = System.uptime
      result("timed prompt, no input") {
        r = Prismfall.timed_choice("Finish copying? (3)", ["Stay.", "Go."], seconds: 3.0, default: 1)
        [r, Prismfall::TimedPrompt.timed_out?, (System.uptime - t0).round(1)]
      }
      spin(10)

      #--- overlays as real sprites -------------------------------------------
      result("lamp board + letterbox") {
        Prismfall::Cutscene.lamp_board([0, 2, 10], [2]); spin(20)
        Prismfall::Cutscene.map_letterbox(true); spin(20)
        ok = [Prismfall::Cutscene.lamp_board_visible?, Prismfall::Cutscene.map_letterbox?]
        Prismfall::Cutscene.clear_map_overlays; spin(5)
        ok + [Prismfall::Cutscene.lamp_board_visible?, Prismfall::Cutscene.map_letterbox?]
      }
      result("hijack hook points on a map without the arena's events") {
        [:HJ_RINGS, :HJ_CRADLE, :HJ_LOCKS, :HJ_CROWN, :HJ_DESCENT, :CH21_VALEN_LIGHT].map { |id| pfm_cutscene(id) }
      }
      result("the white vision's tone") {
        pf_ceremony_vision(hold: 0.2)
        white = $game_screen.tone.red.round
        pf_ceremony_vision_end(10)
        black = $game_screen.tone.red.round
        $game_screen.start_tone_change(Tone.new(0, 0, 0, 0), 0)
        [white, black]
      }
      result("crownhaven walk_to on a real event") {
        e = evs[1]
        PrismfallCrownhaven.walk_to(e, e.x + 2, e.y)
        e.moving? ? :still_moving : :arrived
      }

      #--- the Hush through Game_System ---------------------------------------
      result("hush mute") {
        PrismfallMaps::HUSH_MAPS << 925
        PrismfallMaps.hush_enter
        muted = pfm_hush?
        pbSEPlay("GUI sel decision")
        pbBGMPlay("Battle wild")
        playing = $game_system.playing_bgm
        pfm_hush_lift
        lifted = !pfm_hush?
        PrismfallMaps::HUSH_MAPS.delete(925)
        [muted, playing.nil?, lifted]
      }
      log("done")
    end
  end
end
