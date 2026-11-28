#===============================================================================
# Ch10 "The Seat That Blooms" in the real engine, dev tool (mapgen/layouts/story_ch10.py on the Verdance maps,
# mapgen/puzzles/heartgarden.py for Gym 9). Walks CH10_STEP on the BUILT maps:
#   261 "Morning" (Nell, Juno's note; CH9_STEP 12, CH10_STEP 0) -> out through the Mandate scanner arch ->
#   [by hand: 692 / 680 / 690 are not built: the Lift Road branch and Kestrel's envelope, CH10_STEP 2] -> 284 the
#   Kingsgate arrival (-> 3, S165, V106 1) -> 280 -> 283 (the new inbound warp) -> the gym's doors shut -> 294 "Three
#   Claimants" (-> 4) -> "She's Listening" (-> 5) -> [by hand: 708 the Bride Grove is not built: :ch10_ogre, S127,
#   S125, V106 2, S165 off, CH10_STEP 8] -> Gym 9 WALKED (290 -> 291 -> 292 on the solver's waterings) -> 293 J3
#   (-> 9) -> out: "Little Gardener" on 294 (:ch10_succession_stance, -> 10) -> 280 the royal herald (S126) ->
#   [by hand: 682 the Royal Chase is not built: CH10_STEP 11] -> 281 the cot -> "Dear Uncle Rowan" (-> 12,
#   STORY_CHAPTER 11) -> 281.
# Battles are auto-won; CH10_CHOICES picks the prompts in order ("You Knew", Juno at the tree, the press), default 0,0,2;
# the gym's watering prompts answer Yes. CH10_SHOTS=1 records the key beats (every 45th frame) into frames/ch10_*;
# delete frames/ch10_* and captures_keep/ch10_* after.
#   cp maps_out/Data/Map{261,280,281,283,284,290,291,292,293,294}.rxdata maps_out/Data/system_prismfall.txt \
#      /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch10/010_Ch10StoryCapture.rb --plan ch10story
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch10story")
  module Ch10Cap
    @choices = (ENV["CH10_CHOICES"] || "0,0,2").split(",").map(&:to_i)
    @battles = []
    @gym = false
    class << self; attr_accessor :choices, :battles, :gym; end
    # the solver's waterings (mapgen/puzzles/heartgarden.py): spigot event names, in order
    WATER = {
      290 => ["Spigot P0"],
      291 => ["Spigot P2", "Spigot P6"],
      292 => (ENV["CH10_W292"] || "Spigot A1,Spigot A1,Spigot A1,Spigot A4,Spigot B2,Spigot B2,Spigot B4").split(",")
    }
  end
  class << DemoRun
    def c10_run(limit, min = 30)
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

    def c10_idle?; return !c10_busy?; end

    def c10_fail(msg)
      log("FAIL #{msg}")
      self.auto = false
      stop
      log("done")
      exit
    end

    def c10_goto(map, x, y, dir)
      $game_temp.player_new_map_id = map; $game_temp.player_new_x = x; $game_temp.player_new_y = y
      $game_temp.player_new_direction = dir; $game_temp.player_transferring = true
      c10_run(300, 5) { $game_map.map_id == map && !$game_temp.player_transferring }
    end

    def c10_busy?
      return $game_system.map_interpreter.running? || $game_temp.player_transferring || $game_player.moving? ||
             $game_player.move_route_forcing || $game_temp.message_window_showing || $game_temp.in_battle ||
             $game_map.events.values.any?(&:starting)
    end

    C10_DIRS = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }

    def c10_route(tx, ty)
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
        C10_DIRS.each do |d, (dx, dy)|
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
    def c10_walk(tx, ty, how = :use, limit = 5000)
      map0 = $game_map.map_id
      f = 0; stuck = 0; acting = false; seen = false
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        return [false, f] if f > limit
        busy = c10_busy?
        seen = true if busy && acting
        next if busy
        if acting
          next if !seen && $game_map.map_id == map0 && f < limit
          return [true, f]
        end
        d = c10_route(tx, ty)
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
    C10_KEY = { "U" => 8, "D" => 2, "L" => 4, "R" => 6 }
    def c10_replay(label, route)
      c10_fail("no route for #{label}") if route.to_s.empty?
      route.each_char.with_index do |ch, i|
        c10_run(600, 1) { c10_idle? }
        $PokemonMap.strengthUsed = true if $PokemonMap          # Strength is out (the boulders' own check)
        d = C10_KEY[ch.upcase]
        if ch == ch.upcase
          x0, y0 = $game_player.x, $game_player.y
          $game_player.move_generic(d)
          c10_run(600, 1) { c10_idle? }
          moved = ($game_player.x != x0 || $game_player.y != y0)
          log("RESULT #{label} step #{i} #{ch}: did not move at #{x0},#{y0}") if !moved
        else
          $game_player.turn_generic(d)
          c10_run(10, 2) { true }
          $game_player.instance_variable_set(:@c10_use, true)
          c10_run(900, 50) { c10_idle? }
        end
      end
      c10_run(600, 1) { c10_idle? }
      log("RESULT #{label}: route #{route.length} done at #{$game_player.x},#{$game_player.y} map=#{$game_map.map_id} " \
          "S340-344=#{(340..344).map { |s| $game_switches[s] ? 1 : 0 }.join} rounds=#{$game_variables[340]} pushes=#{$game_variables[341]}")
    end

    def c10_ev(name); return $game_map.events.values.find { |e| e.name == name }; end
    def c10_selfsw(name, ch = "A")
      ev = c10_ev(name)
      return nil if !ev
      return $game_self_switches[[$game_map.map_id, ev.id, ch]]
    end
    def c10_at(*names); return names.map { |n| e = c10_ev(n); "#{n}:#{e&.x},#{e&.y}#{(e && e.character_name.to_s == '') ? '(hidden)' : ''}" }.join(" "); end

    def c10_names
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

    def c10_shot(name); record(name) if ENV["CH10_SHOTS"] == "1"; end

    def c10_water(mid, exit_xy)
      Ch10Cap::WATER[mid].each do |name|
        e = c10_ev(name)
        c10_fail("#{mid}: no spigot #{name}") if !e
        ok, f = c10_walk(e.x, e.y, :use)
        log("RESULT #{mid} #{name}: ok=#{ok} V345=#{$game_variables[345]} S345-348=#{(345..348).map { |s| $game_switches[s] ? 1 : 0 }.join}")
      end
      ok, f = c10_walk(exit_xy[0], exit_xy[1], :touch)
      c10_run(300, 5) { c10_idle? }
      log("RESULT #{mid} out: ok=#{ok} map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch10 story capture boot ok; choices #{Ch10Cap.choices.inspect}")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      c10_names
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 49, [:SURF, :EARTHQUAKE, :STRENGTH, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 49, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      8.times { |i| $player.badges[i] = true }
      { :ch2_tamsin => (ENV["CH10_TAMSIN"] || "keep_secret").to_sym, :ch7_ledger => :reassure, :ch9_teo_sable => :save_teo,
        :ch9_rowan_words => :look_after, :pro_fellowship => :accept }.each { |k, v| pf_choose(k, v) }
      $game_switches[122] = true; $game_switches[123] = true; $game_switches[124] = true
      $game_switches[182] = true if ENV["CH10_VENAM"] == "1"
      $game_variables[130] = 12; $game_variables[101] = 3; $game_variables[102] = 10; $game_variables[131] = 0
      $game_map.setup(261)
      $game_player.moveto(7, 6); $game_player.turn_down
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = 45
      self.auto = true
      t0 = System.uptime
      # --- 261: "Morning"
      f = c10_run(4000) { c10_selfsw("Morning") && c10_idle? }
      log("RESULT morning: selfA=#{c10_selfsw('Morning').inspect} quest=#{($PokemonGlobal.pf_quests[:eighteen_roads] rescue nil).inspect} frames=#{f}")
      c10_fail("Morning did not play") if !c10_selfsw("Morning")
      ok, f = c10_walk(7, 9, :touch)
      log("RESULT scanner arch: seen=#{pfm?(:pc_arch).inspect} map=#{$game_map.map_id}")
      # --- by hand: 692 / 680 / 690 (the Lift Road and Kestrel's envelope) are not built
      $game_variables[131] = 2
      c10_goto(284, 19, 21, 8)
      c10_shot("ch10_arrival")
      f = c10_run(4000) { $game_variables[131] >= 3 && c10_idle? }
      stop
      log("RESULT kingsgate: CH10_STEP=#{$game_variables[131]} S165=#{$game_switches[165]} V106=#{$game_variables[106]} frames=#{f}")
      c10_fail("the Kingsgate arrival did not reach 3") if $game_variables[131] < 3
      # --- up through the Market Terraces (the new inbound warps) to the Glasshouse Ward
      ok, f = c10_walk(19, 6, :touch); c10_run(300, 5) { $game_map.map_id == 280 && c10_idle? }
      log("RESULT 284 -> 280: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      ok, f = c10_walk(58, 70, :use); log("RESULT florist: ok=#{ok}")
      ok, f = c10_walk(99, 66, :touch, 8000); c10_run(300, 5) { $game_map.map_id == 283 && c10_idle? }
      log("RESULT 280 -> 283: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      ok, f = c10_walk(24, 9, :touch)
      log("RESULT gym doors at 3: map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      c10_fail("the gym let the player in before the Plate") if $game_map.map_id != 283
      ok, f = c10_walk(45, 10, :use); log("RESULT thornguard: ok=#{ok}")
      # --- 294: "Three Claimants" (-> 4), "She's Listening" (-> 5)
      c10_shot("ch10_testament")
      ok, f = c10_walk(46, 12, :touch); c10_run(300, 5) { $game_map.map_id == 294 }
      f = c10_run(12000) { $game_variables[131] >= 4 && c10_idle? }
      log("RESULT three claimants: CH10_STEP=#{$game_variables[131]} map=#{$game_map.map_id} frames=#{f}")
      c10_fail("Three Claimants did not reach 4") if $game_variables[131] < 4
      ok, f = c10_walk(19, 22, :use)
      stop
      log("RESULT she's listening: CH10_STEP=#{$game_variables[131]} ok=#{ok}")
      c10_fail("She's Listening did not reach 5") if $game_variables[131] < 5
      ok, f = c10_walk(19, 34, :touch); log("RESULT the stairhead (708 not built): map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y}")
      # --- by hand: 708 the Bride Grove is not built
      pf_choose(:ch10_ogre, :ogre); $game_switches[127] = true; $game_switches[125] = true
      $game_variables[106] = 2; $game_switches[165] = false; $game_variables[131] = 8
      log("RESULT by hand (708): ch10_ogre=#{pf_choice(:ch10_ogre).inspect} S125=#{$game_switches[125]} CH10_STEP=8")
      # --- Gym 9
      c10_goto(283, 24, 10, 8)
      ok, f = c10_walk(24, 9, :touch); c10_run(300, 5) { $game_map.map_id == 290 && c10_idle? }
      log("RESULT gym doors at 8: map=#{$game_map.map_id}")
      c10_fail("the gym's doors did not open at 8") if $game_map.map_id != 290
      ok, f = c10_walk(6, 13, :use); log("RESULT gym guide: ok=#{ok}")
      Ch10Cap.gym = true
      c10_water(290, [10, 4])
      c10_water(291, [14, 4])
      c10_water(292, [14, 4])
      Ch10Cap.gym = false
      c10_fail("not in the Warden Arena") if $game_map.map_id != 293
      c10_shot("ch10_j3")
      ok, f = c10_walk(10, 5, :use)
      stop
      log("RESULT J3: CH10_STEP=#{$game_variables[131]} badge9=#{$player.badges[8].inspect} TM53=#{$bag.quantity(:TM53)} V345=#{$game_variables[345]} " \
          "battles=#{Ch10Cap.battles.inspect} frames=#{f}")
      c10_fail("J3 did not reach 9") if $game_variables[131] < 9 || !$player.badges[8]
      # --- out of the gym: "Little Gardener" on 294
      c10_goto(283, 24, 10, 2)
      c10_shot("ch10_gardener")
      f = c10_run(12000) { $game_variables[131] >= 10 && c10_idle? }
      stop
      log("RESULT little gardener: CH10_STEP=#{$game_variables[131]} map=#{$game_map.map_id} stance=#{pf_choice(:ch10_succession_stance).inspect} frames=#{f}")
      c10_fail("Little Gardener did not reach 10") if $game_variables[131] < 10
      # --- 280: the herald (S126); by hand 682 (the Chase) -> 11; 281: the night
      c10_goto(280, 50, 66, 8)
      f = c10_run(3000) { $game_switches[126] && c10_idle? }
      log("RESULT herald: S126=#{$game_switches[126]} frames=#{f}")
      $game_variables[131] = 11
      log("RESULT by hand (682): CH10_STEP=11")
      c10_goto(281, 7, 8, 8)
      c10_shot("ch10_night")
      f = c10_run(8000, 60) { $game_variables[131] >= 12 && $game_map.map_id == 281 && c10_idle? }
      stop
      log("RESULT dear uncle rowan: CH10_STEP=#{$game_variables[131]} STORY_CHAPTER=#{$game_variables[102]} map=#{$game_map.map_id} " \
          "quest=#{($PokemonGlobal.pf_quests[:eighteen_roads] rescue nil).inspect} secs=#{(System.uptime - t0).round(1)}")
      c10_fail("the chapter did not close") if $game_variables[131] < 12 || $game_variables[102] != 11
      c10_run(60, 60) { true }
      self.auto = false
      stop
      log("done")
    end
  end
  # every change of CH10_STEP as it happens (which map, which event)
  module Graphics
    @c10_step = nil
    class << self
      alias c10_update update unless method_defined?(:c10_update)
      def update
        c10_update
        if $game_variables && DemoRun.started && $game_variables[131] != @c10_step
          DemoRun.log("RESULT step #{@c10_step.inspect} -> #{$game_variables[131]} on map #{$game_map&.map_id} " \
                      "(event #{$game_system.map_interpreter.instance_variable_get(:@event_id) rescue '?'})") if !@c10_step.nil?
          @c10_step = $game_variables[131]
        end
      end
    end
  end
  module Input
    class << self
      alias c10_trigger? trigger? unless method_defined?(:c10_trigger?)
      def trigger?(button)
        if button == Input::USE && DemoRun.auto
          if $game_player && $game_player.instance_variable_get(:@c10_use)     # a route's use: one press, now
            $game_player.instance_variable_set(:@c10_use, false)
            @c10_used = DemoRun.frame
            return true
          end
          return false if DemoRun.frame % 45 != 0 || @c10_used == DemoRun.frame
          @c10_used = DemoRun.frame
          return true
        end
        return c10_trigger?(button)
      end
    end
  end
  alias c10_pbShowCommands pbShowCommands unless defined?(c10_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = Ch10Cap.gym ? 0 : (Ch10Cap.choices.shift || 0)
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return c10_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias c10_pbCommandPhase pbCommandPhase unless method_defined?(:c10_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        DemoRun.log("battle vs #{names.join(' + ')}")
        Ch10Cap.battles << names
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      c10_pbCommandPhase
    end
  end
end
