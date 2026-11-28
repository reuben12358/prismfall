#===============================================================================
# Ch9 "The Iron Conclave" in the real engine, dev tool (mapgen/layouts/story_ch9.py on Gemini's Ironreach maps,
# mapgen/puzzles/pit.py for Gym 8). Walks CH9_STEP on the BUILT maps:
#   2 (set by hand: 660 the Ashmarch and 672 the Long Drop are not built) -> 260 arrival at the cage-foot -> the Pit's
#   door is shut -> 263 "The Conclave Opens" (-> 3) -> free roam (Juno and Rowan, the envoys, Celestine) -> Nell:
#   "The Bracket" -> Kestrel and his Scizor (-> 4) -> Nell: the Open (three rounds) and K4 (-> 5, S122) -> 260's Pit
#   door -> Gym 8 WALKED (270 -> 271 -> 272 -> 273 -> 274) on the solver's routes (puzzles/pit.py SOLUTIONS) ->
#   Kaito (-> 6) -> Odessa's Fly -> 263 "The Vote" + the tag battle (-> 7) -> [by hand: 264 the Reliquary is not built:
#   S124, CH9_STEP 8, :ch9_teo_sable, 9] -> 263 "Mandate Jurisdiction" (:ch9_rowan_words, -> 10, S123) -> "A Seat to
#   Fill" (-> 11) -> 261 the night bulletin -> Interlude II on 294 (the tree, Glasswood, the shed, the stair) ->
#   END OF ACT II (CH9_STEP 12, STORY_ACT 3, STORY_CHAPTER 10) -> 261.
# Battles are auto-won; CH9_CHOICES picks the prompts in order (Celestine, Rowan's words), default 0,1; CH9_TEO
# (save_teo | chase_sable) sets the 264 choice. CH9_SHOTS=1 records the key beats (every 45th frame) into
# frames/ch9_*; delete frames/ch9_* and captures_keep/ch9_* after. RESULT lines in demo.log; a stage that fails
# stops the run (FAIL).
#   cp maps_out/Data/Map{260,261,262,263,270,271,272,273,274,294}.rxdata maps_out/Data/system_prismfall.txt \
#      /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch9/010_Ch9StoryCapture.rb --plan ch9story
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch9story")
  module Ch9Cap
    @choices = (ENV["CH9_CHOICES"] || "0,1").split(",").map(&:to_i)
    @battles = []
    @gym = false
    class << self; attr_accessor :choices, :battles, :gym; end
    # the solver's routes (mapgen/puzzles/pit.py; regenerate after Gemini changes 271-273): U/D/L/R a step,
    # u/d/l/r face that way and use (a push or a bell)
    ROUTES = {
      "271w" => "LLLLLULUUURUULLLLUUUUUUURRUUUu",
      "271e" => "RRRRRRRUUUUUUUUULLLLUUUUUUUUUUUUUURRDRr",
      "272"  => "LLUURUULUULLLLLLuUuULRuRRRRRRRUURLLLLLLLDLuDRRRRRRRRRURRRRRRUDDDDRuUuULRRUULLUULDDDRDRuLLLLLLLLRRUULLu",
      "273"  => (ENV["CH9_R273"] || "LUUULLUUUULUrRrRrUUUUUDDLLLULUUUrRURRRRD")
    }
  end
  class << DemoRun
    def c9_run(limit, min = 30)
      f = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        break if f > limit
        break if f > min && yield
      end
      return f
    end

    def c9_idle?; return !c9_busy?; end

    def c9_fail(msg)
      log("FAIL #{msg}")
      self.auto = false
      stop
      log("done")
      exit
    end

    def c9_goto(map, x, y, dir)
      $game_temp.player_new_map_id = map; $game_temp.player_new_x = x; $game_temp.player_new_y = y
      $game_temp.player_new_direction = dir; $game_temp.player_transferring = true
      c9_run(300, 5) { $game_map.map_id == map && !$game_temp.player_transferring }
    end

    def c9_busy?
      return $game_system.map_interpreter.running? || $game_temp.player_transferring || $game_player.moving? ||
             $game_player.move_route_forcing || $game_temp.message_window_showing || $game_temp.in_battle ||
             $game_map.events.values.any?(&:starting)
    end

    C9_DIRS = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }

    def c9_route(tx, ty)
      blocked = {}
      $game_map.events.each_value do |e|
        next if e.through || (e.x == tx && e.y == ty)
        blocked[[e.x, e.y]] = true if e.character_name.to_s != "" || e.tile_id > 0 || e.trigger == 1
      end
      start = [$game_player.x, $game_player.y]
      near = ->(c) { (c[0] - tx).abs + (c[1] - ty).abs == 1 }
      return 0 if near.call(start)
      first = { start => nil }
      q = [start]
      until q.empty?
        c = q.shift
        C9_DIRS.each do |d, (dx, dy)|
          n = [c[0] + dx, c[1] + dy]
          next if first.key?(n) || blocked[n] || !$game_player.passable?(c[0], c[1], d)
          first[n] = first[c] || d
          return first[n] if near.call(n)
          q << n
        end
      end
      return nil
    end

    # walk next to (tx, ty) and use it (:use) or step onto it (:touch); waits for whatever it starts to finish
    def c9_walk(tx, ty, how = :use, limit = 5000)
      map0 = $game_map.map_id
      f = 0; stuck = 0; acting = false; seen = false
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        return [false, f] if f > limit
        busy = c9_busy?
        seen = true if busy && acting
        next if busy
        if acting
          next if !seen && $game_map.map_id == map0 && f < limit
          return [true, f]
        end
        d = c9_route(tx, ty)
        if d.nil?
          stuck += 1
          return [false, f] if stuck > 90
          next
        end
        stuck = 0
        if d == 0
          dx, dy = tx - $game_player.x, ty - $game_player.y
          dir = (dx > 0) ? 6 : (dx < 0) ? 4 : (dy > 0) ? 2 : 8
          acting = true
          if how == :touch then $game_player.move_generic(dir) else $game_player.turn_generic(dir) end
          next
        end
        $game_player.move_generic(d)
      end
    end

    # replay a solver route (puzzles/pit.py) step by step, exactly as the proof walked it
    C9_KEY = { "U" => 8, "D" => 2, "L" => 4, "R" => 6 }
    def c9_replay(label, route)
      c9_fail("no route for #{label}") if route.to_s.empty?
      route.each_char.with_index do |ch, i|
        c9_run(600, 1) { c9_idle? }
        $PokemonMap.strengthUsed = true if $PokemonMap          # Strength is out (the boulders' own check)
        d = C9_KEY[ch.upcase]
        if ch == ch.upcase
          x0, y0 = $game_player.x, $game_player.y
          $game_player.move_generic(d)
          c9_run(600, 1) { c9_idle? }
          moved = ($game_player.x != x0 || $game_player.y != y0)
          log("RESULT #{label} step #{i} #{ch}: did not move at #{x0},#{y0}") if !moved
        else
          $game_player.turn_generic(d)
          c9_run(10, 2) { true }
          $game_player.instance_variable_set(:@c9_use, true)
          c9_run(900, 50) { c9_idle? }
        end
      end
      c9_run(600, 1) { c9_idle? }
      log("RESULT #{label}: route #{route.length} done at #{$game_player.x},#{$game_player.y} map=#{$game_map.map_id} " \
          "S340-344=#{(340..344).map { |s| $game_switches[s] ? 1 : 0 }.join} rounds=#{$game_variables[340]} pushes=#{$game_variables[341]}")
    end

    def c9_ev(name); return $game_map.events.values.find { |e| e.name == name }; end
    def c9_selfsw(name, ch = "A")
      ev = c9_ev(name)
      return nil if !ev
      return $game_self_switches[[$game_map.map_id, ev.id, ch]]
    end
    def c9_at(*names); return names.map { |n| e = c9_ev(n); "#{n}:#{e&.x},#{e&.y}#{(e && e.character_name.to_s == '') ? '(hidden)' : ''}" }.join(" "); end

    def c9_names
      File.foreach("Data/system_prismfall.txt") do |l|
        next if l.start_with?("#")
        kind, id, name = l.chomp.split("\t", 3)
        next if !name
        list = (kind == "S") ? $data_system.switches : $data_system.variables
        list[id.to_i] = name if list[id.to_i].to_s.empty?
      end
    rescue StandardError => e
      log("names: #{e.message}")
    end

    def c9_shot(name); record(name) if ENV["CH9_SHOTS"] == "1"; end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch9 story capture boot ok; choices #{Ch9Cap.choices.inspect}")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      c9_names
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 45, [:SURF, :EARTHQUAKE, :STRENGTH, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 45, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      7.times { |i| $player.badges[i] = true }
      # the earlier chapters' keys (Core choices) the scenes branch on
      { :ch2_tamsin => :expose, :ch3_juno_talk => :told, :ch4_teo => :keep_secret, :ch5_lowlight_testimony => :mourner,
        :ch6_drillsite => :sanctuary, :ch6_kestrel_rumor => :warn, :ch7_ledger => :reassure, :ch8_caldera => :shutdown
      }.each { |k, v| pf_choose(k, v) }
      $game_variables[102] = 9
      $game_variables[130] = 2                         # by hand: 660 (Larch, -> 1) and 672 (the cage, -> 2) are not built
      $game_map.setup(260)
      $game_player.moveto(20, 9); $game_player.turn_down
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = 45
      self.auto = true
      t0 = System.uptime
      # --- 260: arrival at the cage-foot (2)
      f = c9_run(3000) { c9_selfsw("Ironreach Arrival") && c9_idle? }
      log("RESULT arrival: selfA=#{c9_selfsw('Ironreach Arrival').inspect} pos=#{$game_player.x},#{$game_player.y} frames=#{f}")
      c9_fail("the arrival did not play") if !c9_selfsw("Ironreach Arrival")
      ok, f = c9_walk(21, 36, :touch)
      log("RESULT pit door at CH9_STEP 2: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} frames=#{f}")
      c9_fail("the Pit let the player in before K4") if $game_map.map_id != 260
      # --- 263: "The Conclave Opens" (2 -> 3)
      c9_goto(263, 20, 31, 8)
      c9_shot("ch9_rollcall")
      f = c9_run(9000) { $game_variables[130] >= 3 && c9_idle? }
      stop
      log("RESULT roll-call: CH9_STEP=#{$game_variables[130]} #{c9_at('Hollis', 'Valen', 'Odessa', 'Rowan', 'Juno (with Rowan)', 'Kaito', 'Ysolde')} frames=#{f}")
      c9_fail("the roll-call did not reach 3") if $game_variables[130] < 3
      # --- free roam: Juno and Rowan, the envoys, Celestine
      ok, f = c9_walk(18, 10, :use); log("RESULT juno+rowan: ok=#{ok} ring=#{pfm?(:ch9_juno_rowan).inspect} frames=#{f}")
      ok, f = c9_walk(21, 2, :use); log("RESULT anja+envoys: ok=#{ok} lease=#{pfm?(:ch9_lease).inspect} #{c9_at('Envoy of Ossaria')} frames=#{f}")
      ok, f = c9_walk(28, 10, :use); log("RESULT celestine: ok=#{ok} frames=#{f}")
      # --- "The Bracket" (Nell), then Kestrel by the Pit's wall (-> 4)
      ok, f = c9_walk(16, 28, :use)
      log("RESULT bracket: ok=#{ok} bracket=#{pfm?(:ch9_bracket).inspect} kestrelA=#{c9_selfsw('Kestrel').inspect} frames=#{f}")
      ok, f = c9_walk(23, 26, :use)
      log("RESULT kestrel: CH9_STEP=#{$game_variables[130]} #{c9_at('Kestrel', 'Scizor')} frames=#{f}")
      c9_fail("Kestrel did not move the step to 4") if $game_variables[130] < 4
      # --- the Open and K4 (-> 5)
      n0 = Ch9Cap.battles.length
      c9_shot("ch9_open")
      ok, f = c9_walk(16, 28, :use, 20000)
      stop
      log("RESULT the open + K4: CH9_STEP=#{$game_variables[130]} S122=#{$game_switches[122]} rounds=#{[1, 2, 3].map { |i| pfm?("ch9_open#{i}".to_sym) ? 1 : 0 }.join} " \
          "chalk=#{pfm_has?(:OPENCHAMPIONSCHALK).inspect} ysolde=#{c9_at('Ysolde')} battles=#{Ch9Cap.battles[n0..-1].inspect} frames=#{f}")
      c9_fail("K4 did not reach 5") if $game_variables[130] < 5
      # --- Gym 8, walked on the solver's routes
      c9_goto(260, 21, 37, 8)
      ok, f = c9_walk(21, 36, :touch)
      c9_run(300, 5) { $game_map.map_id == 270 && c9_idle? }
      log("RESULT pit door at CH9_STEP 5: map=#{$game_map.map_id}")
      c9_fail("the Pit's door did not open at 5") if $game_map.map_id != 270
      ok, f = c9_walk(7, 13, :use); log("RESULT gym guide: ok=#{ok}")
      Ch9Cap.gym = true
      ok, f = c9_walk(10, 4, :touch); c9_run(300, 5) { $game_map.map_id == 271 && c9_idle? }
      log("RESULT into 271: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      c9_replay("271 west", Ch9Cap::ROUTES["271w"])
      c9_fail("271 west bell not rung") if !$game_switches[344]
      ok, f = c9_walk(14, 23, :use)            # back to the foot of the room (next to the door mat)
      c9_goto(271, 14, 22, 8) if [$game_player.x, $game_player.y] != [14, 22]
      c9_replay("271 east", Ch9Cap::ROUTES["271e"])
      c9_fail("271 east bell not rung") if !$game_switches[340]
      ok, f = c9_walk(24, 4, :touch); c9_run(300, 5) { $game_map.map_id == 272 && c9_idle? }
      log("RESULT into 272: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      c9_replay("272", Ch9Cap::ROUTES["272"])
      c9_fail("272 bell not rung") if !$game_switches[341]
      ok, f = c9_walk(14, 4, :touch); c9_run(300, 5) { $game_map.map_id == 273 && c9_idle? }
      log("RESULT into 273: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      c9_replay("273", Ch9Cap::ROUTES["273"])
      c9_fail("273 plates not held") if !$game_switches[342]
      ok, f = c9_walk(10, 4, :touch); c9_run(300, 5) { $game_map.map_id == 274 && c9_idle? }
      Ch9Cap.gym = false
      n0 = Ch9Cap.battles.length
      ok, f = c9_walk(10, 5, :use)
      log("RESULT kaito: CH9_STEP=#{$game_variables[130]} badge8=#{$player.badges[7].inspect} TM31=#{$bag.quantity(:TM31)} " \
          "battles=#{Ch9Cap.battles.inspect} frames=#{f}")
      c9_fail("Kaito did not reach 6") if $game_variables[130] < 6 || !$player.badges[7]
      c9_goto(270, 12, 15, 8)
      ok, f = c9_walk(12, 14, :use)
      log("RESULT odessa: HM02=#{$bag.quantity(:HM02)} fly=#{pfm?(:ch9_fly).inspect}")
      # --- 263: "The Vote" and the tag battle (6 -> 7)
      c9_goto(263, 20, 31, 8)
      c9_shot("ch9_vote")
      f = c9_run(12000) { $game_variables[130] >= 7 && c9_idle? }
      stop
      log("RESULT the vote: CH9_STEP=#{$game_variables[130]} battles=#{Ch9Cap.battles[-1].inspect} #{c9_at('Rubble 2', 'Corvin', 'Kestrel (bench)')} tone=#{$game_screen.tone.red.round} frames=#{f}")
      c9_fail("The Vote did not reach 7") if $game_variables[130] < 7
      # --- by hand: 264 the Reliquary is not built (the Mourner, IR-1, S124, :ch9_teo_sable)
      $game_switches[124] = true; $game_variables[130] = 8
      pf_choose(:ch9_teo_sable, (ENV["CH9_TEO"] || "save_teo").to_sym)
      $game_variables[130] = 9
      log("RESULT by hand (264): S124=#{$game_switches[124]} ch9_teo_sable=#{pf_choice(:ch9_teo_sable).inspect} CH9_STEP=9")
      # --- 263: "Mandate Jurisdiction" (9 -> 10) and "A Seat to Fill" (-> 11)
      c9_goto(260, 33, 13, 2)
      c9_goto(263, 20, 31, 8)
      c9_shot("ch9_mandate")
      f = c9_run(15000) { $game_variables[130] >= 11 && c9_idle? }
      stop
      log("RESULT mandate + seat: CH9_STEP=#{$game_variables[130]} S123=#{$game_switches[123]} V113=#{$game_variables[113]} V111=#{$game_variables[111]} " \
          "rowan_words=#{pf_choice(:ch9_rowan_words).inspect} bond_juno=#{(pf_bond(:JUNO) rescue '?')} bond_kestrel=#{(pf_bond(:KESTREL) rescue '?')} " \
          "quest=#{($PokemonGlobal.pf_quests[:eighteen_roads] rescue nil).inspect} frames=#{f}")
      c9_fail("Mandate / Seat did not reach 11") if $game_variables[130] < 11
      # --- 261: the night bulletin; sleep; Interlude II on 294
      c9_goto(261, 7, 9, 8)
      f = c9_run(6000) { $game_map.map_id == 294 && c9_idle? }
      log("RESULT bulletin -> interlude: map=#{$game_map.map_id} V119=#{$game_variables[119]} name=#{$player.name} " \
          "party=#{$player.party.map { |p| p.species }.inspect} pos=#{$game_player.x},#{$game_player.y} frames=#{f}")
      c9_fail("Interlude II did not start") if $game_map.map_id != 294 || $game_variables[119] != 2
      c9_run(600, 30) { c9_idle? }
      ok, f = c9_walk(19, 34, :touch); log("RESULT stair too early: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      ok, f = c9_walk(19, 20, :use); log("RESULT the bride tree: ok=#{ok} done=#{pfm?(:il2_tree).inspect}")
      g = c9_ev("Glasswood")
      ok, f = c9_walk(g.x, g.y, :use) if g; log("RESULT glasswood: ok=#{ok} done=#{pfm?(:il2_trev).inspect} at=#{g&.x},#{g&.y}")
      ok, f = c9_walk(8, 6, :use); log("RESULT the shed: ok=#{ok} done=#{pfm?(:il2_shed).inspect} pos=#{$game_player.x},#{$game_player.y}")
      c9_shot("ch9_interlude")
      ok, f = c9_walk(19, 34, :touch, 8000)
      c9_run(3000, 30) { $game_map.map_id == 261 && c9_idle? }
      stop
      log("RESULT end of act II: map=#{$game_map.map_id} CH9_STEP=#{$game_variables[130]} V119=#{$game_variables[119]} STORY_ACT=#{$game_variables[101]} " \
          "STORY_CHAPTER=#{$game_variables[102]} name=#{$player.name} party=#{$player.party.map { |p| p.species }.inspect} secs=#{(System.uptime - t0).round(1)}")
      c9_fail("Act II did not end") if $game_variables[130] < 12 || $game_variables[101] != 3 || $game_variables[102] != 10
      c9_run(60, 60) { true }
      self.auto = false
      stop
      log("done")
    end
  end
  # every change of CH9_STEP as it happens (which map, which event)
  module Graphics
    @c9_step = nil
    class << self
      alias c9_update update unless method_defined?(:c9_update)
      def update
        c9_update
        if $game_variables && DemoRun.started && $game_variables[130] != @c9_step
          DemoRun.log("RESULT step #{@c9_step.inspect} -> #{$game_variables[130]} on map #{$game_map&.map_id} " \
                      "(event #{$game_system.map_interpreter.instance_variable_get(:@event_id) rescue '?'})") if !@c9_step.nil?
          @c9_step = $game_variables[130]
        end
      end
    end
  end
  module Input
    class << self
      alias c9_trigger? trigger? unless method_defined?(:c9_trigger?)
      def trigger?(button)
        if button == Input::USE && DemoRun.auto
          if $game_player && $game_player.instance_variable_get(:@c9_use)     # a route's use: one press, now
            $game_player.instance_variable_set(:@c9_use, false)
            @c9_used = DemoRun.frame
            return true
          end
          return false if DemoRun.frame % 45 != 0 || @c9_used == DemoRun.frame
          @c9_used = DemoRun.frame
          return true
        end
        return c9_trigger?(button)
      end
    end
  end
  alias c9_pbShowCommands pbShowCommands unless defined?(c9_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = Ch9Cap.gym ? 0 : (Ch9Cap.choices.shift || 0)
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return c9_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias c9_pbCommandPhase pbCommandPhase unless method_defined?(:c9_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        DemoRun.log("battle vs #{names.join(' + ')}")
        Ch9Cap.battles << names
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      c9_pbCommandPhase
    end
  end
end
