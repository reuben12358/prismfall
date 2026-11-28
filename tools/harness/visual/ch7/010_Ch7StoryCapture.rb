#===============================================================================
# Ch7 "The Quiet Ward" in the real engine, dev tool (mapgen/layouts/story_ch7.py on Gemini's 220 / 223 / 230-233).
# Walks CH7_STEP (V127) from 0 to 7. Steps set BY HAND are only the unbuilt maps' own beats:
#   0 -> 1   633 the Gutterfall "Down" (not built)
#   3 -> 4   648 the Weeping Fen, Brother Wick (not built; also S119 CH7_WICK_DONE)
# Everything else is played: 220 arrival (selfA) -> Sweetrot offer 1 (taken) -> the Gym door slate turns you back ->
# 223 "The Quiet Ward" (-> 2) -> Juno: "R.A." + J2 (auto-won) + :ch7_ledger (-> 3, S118) -> 220: offer 2 walks up
# (taken: V128 2, Wenlow's panic) -> [648 by hand] -> 223 "Invoice" -> 220: offer 3 (checkpoint, refused: Mother
# Gutter's barge) -> Gym 6 WALKED (230 teach, 231 four-from-three-and-five, 232 the sludge gallery's two trips, the
# solver's route in mapgen/puzzles/infirmary.py) -> 233 Corvin (auto-won; Remedy Badge, TM84, -> 5) -> 220: the Ward
# Night (roof -> 223 Veil -> roof, -> 6) -> the close (-> 7, STORY_CHAPTER 8).
# Battles are auto-won; story choices come from CH7_CHOICES (0-based, in order: offer 1, the ledger, offer 2,
# Invoice, offer 3), default 0,1,0,0,1 (take, reassure, take, "I'm fine.", refuse). Frames only with CH7_SHOTS=1
# (every 30th, only in the story scenes, not the gym walk; delete frames/ch7_* and captures_keep/ch7_* after).
# RESULT lines in demo.log; a stage that fails stops the run (FAIL).
#   cp maps_out/Data/Map{220,221,222,223,230,231,232,233}.rxdata maps_out/Data/system_prismfall.txt /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch7/010_Ch7StoryCapture.rb --plan ch7story
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch7story")
  module Ch7Cap
    @choices = (ENV["CH7_CHOICES"] || "0,1,0,0,1").split(",").map(&:to_i)
    @battles = []
    @gym = false          # in the gym: every prompt takes the next of @picks, else its last option
    @picks = []
    class << self; attr_accessor :choices, :battles, :gym, :picks; end
  end
  class << DemoRun
    def c7_run(limit, min = 30)
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

    def c7_idle?; return !$game_system.map_interpreter.running? && !$game_temp.player_transferring && !$game_player.moving?; end

    def c7_fail(msg)
      log("FAIL #{msg}")
      self.auto = false
      stop
      log("done")
      exit
    end

    def c7_goto(map, x, y, dir)
      $game_temp.player_new_map_id = map; $game_temp.player_new_x = x; $game_temp.player_new_y = y
      $game_temp.player_new_direction = dir; $game_temp.player_transferring = true
      c7_run(300, 5) { $game_map.map_id == map && !$game_temp.player_transferring }
    end

    def c7_busy?
      return $game_system.map_interpreter.running? || $game_temp.player_transferring || $game_player.moving? ||
             $game_player.move_route_forcing || $game_temp.message_window_showing || $game_temp.in_battle ||
             $game_map.events.values.any?(&:starting)
    end

    C7_DIRS = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }
    C7_WALKABLE = /\A(Sludge \d|Sludge Sluice Gate|Arena Bridge|Dispensary Bridge|Teach Bridge|Gym door slate|Ward Night)/

    # the first step toward a tile next to (tx, ty), round every event tile but the walkable ones (sludge, bridges,
    # the gate: the engine's passable? decides those); 0 = there already, nil = no way
    def c7_route(tx, ty)
      blocked = {}
      $game_map.events.each_value do |e|
        next if e.name =~ C7_WALKABLE || (e.x == tx && e.y == ty)
        next if e.character_name.to_s == "" && e.tile_id.to_i == 0 && e.through && e.trigger != 1 && e.trigger != 2
        blocked[[e.x, e.y]] = true
      end
      start = [$game_player.x, $game_player.y]
      near = ->(c) { (c[0] - tx).abs + (c[1] - ty).abs == 1 }
      return 0 if near.call(start)
      first = { start => nil }
      q = [start]
      until q.empty?
        c = q.shift
        C7_DIRS.each do |d, (dx, dy)|
          n = [c[0] + dx, c[1] + dy]
          next if first.key?(n) || blocked[n] || !$game_player.passable?(c[0], c[1], d)
          first[n] = first[c] || d
          return first[n] if near.call(n)
          q << n
        end
      end
      return nil
    end

    # walk to (tx, ty) and use it (:use) or walk into it (:touch); picks = the answers to its prompts -> [ok, frames]
    # `seen` only counts the TARGET's own event running (or a new map): a trainer who spots you on the way is fought
    # and the walk goes on; an action that nothing answered for 90 idle frames is tried again
    def c7_walk(tx, ty, how = :use, picks = [], limit = 5000)
      map0 = $game_map.map_id
      target = $game_map.events.values.find { |e| e.x == tx && e.y == ty }
      f = 0; stuck = 0; acting = false; seen = false; waited = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        return [false, f] if f > limit
        busy = c7_busy?
        if busy && acting
          run_id = $game_system.map_interpreter.instance_variable_get(:@event_id)
          seen = true if $game_map.map_id != map0 || !target || run_id == target.id
        end
        next if busy
        if acting
          if !seen && $game_map.map_id == map0
            waited += 1
            if waited > 90
              acting = false; waited = 0
            end
            next
          end
          Ch7Cap.picks = []
          return [true, f]
        end
        d = c7_route(tx, ty)
        if d.nil?
          stuck += 1
          if stuck > 90
            col = (ty - 6..ty + 6).map { |y| "#{tx},#{y}:#{$game_player.passable?(tx, y + 1, 8) ? 'u' : '-'}#{$game_map.passable?(tx, y, 2) ? 'd' : '-'}" }
            evs = $game_map.events.values.select { |e| (e.x - tx).abs <= 2 && (e.y - ty).abs <= 6 }.map { |e| "#{e.name}@#{e.x},#{e.y}:t#{e.tile_id}/#{e.through}" }
            log("stuck to #{tx},#{ty} from #{$game_player.x},#{$game_player.y}: #{col.join(' ')} | #{evs.join('; ')}")
            return [false, f]
          end
          next
        end
        stuck = 0
        if d == 0
          dx, dy = tx - $game_player.x, ty - $game_player.y
          dir = (dx > 0) ? 6 : (dx < 0) ? 4 : (dy > 0) ? 2 : 8
          Ch7Cap.picks = picks.dup
          acting = true; waited = 0
          if how == :touch
            $game_player.move_generic(dir)
          else
            $game_player.turn_generic(dir)
          end
          next
        end
        $game_player.move_generic(d)
      end
    end

    def c7_g6_state
      "map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} flasks=#{$game_variables[330]}/#{$game_variables[331]} " \
        "filter=#{$game_variables[332]} basin=#{$game_variables[333]} S330-334=#{(330..334).map { |i| $game_switches[i] ? 1 : 0 }.join}"
    end

    def c7_g6(label, map, tx, ty, how, picks = [], want = nil)
      c7_fail("#{label}: on map #{$game_map.map_id}, not #{map}") if $game_map.map_id != map
      ok, f = c7_walk(tx, ty, how, picks)
      log("RESULT g6 #{label}: ok=#{ok} #{c7_g6_state} frames=#{f}")
      c7_fail("#{label} did not finish") if !ok
      c7_fail("#{label}: ended on map #{$game_map.map_id}, not #{want}") if want && $game_map.map_id != want
    end

    def c7_selfsw(name, ch = "A")
      ev = $game_map.events.values.find { |e| e.name == name }
      return nil if !ev
      return $game_self_switches[[$game_map.map_id, ev.id, ch]]
    end

    def c7_names
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

    # one frame folder for the whole run; record() resets the frame counter, so keep the numbering across segments
    def c7_shots(on)
      return if ENV["CH7_SHOTS"] != "1"
      if on
        record("ch7_story")
        @shots = @c7_kept if @c7_kept
      else
        @c7_kept = @shots
        stop
      end
    end

    def c7_state
      "V127=#{$game_variables[127]} V128=#{$game_variables[128]} S118=#{$game_switches[118]} S119=#{$game_switches[119]} " \
        "map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} shot=#{@shots.inspect}"
    end

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch7 story capture boot ok; choices #{Ch7Cap.choices.inspect}")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      c7_names
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 35, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 35, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      5.times { |i| $player.badges[i] = true }
      $game_variables[102] = 7
      $game_variables[127] = 1                         # BY HAND: 633 "Down" (not built) sets 0 -> 1
      log("RESULT by hand: V127 0 -> 1 (633 the Gutterfall is not built)")
      $game_map.setup(220)
      $game_player.moveto(15, 6); $game_player.turn_down
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = [(ENV["CH7_EVERY"] || 30).to_i, 15].max
      self.auto = true
      t0 = System.uptime
      if ENV["CH7_FROM"] == "gym"                      # debug shortcut: the first half's state, set by hand
        $game_variables[127] = 4; $game_variables[128] = 2; $game_switches[118] = true; $game_switches[119] = true
        pf_choose(:ch7_ledger, :reassure) rescue nil
        log("RESULT by hand (CH7_FROM=gym): V127 4, V128 2, S118, S119, :ch7_ledger :reassure")
        return c7_second_half(t0)
      end
      if ENV["CH7_FROM"] == "ward"                     # debug shortcut: through Gym 6, set by hand
        $game_variables[127] = 5; $game_variables[128] = 1; $game_switches[118] = true; $game_switches[119] = true
        $player.badges[5] = true
        pf_choose(:ch7_ledger, :reassure) rescue nil
        log("RESULT by hand (CH7_FROM=ward): V127 5, V128 1, S118, S119, badge 6, :ch7_ledger :reassure")
        c7_shots(true)
        return c7_ward(t0)
      end
      c7_shots(true)
      # --- 220: the arrival
      f = c7_run(3000) { c7_selfsw("Arrival (Mirefen)") && c7_idle? }
      log("RESULT arrival: selfA=#{c7_selfsw('Arrival (Mirefen)').inspect} #{c7_state} frames=#{f}")
      c7_fail("the arrival did not play") if !c7_selfsw("Arrival (Mirefen)")
      # --- offer 1 at the Sweet Market
      ok, f = c7_walk(21, 31, :use)
      log("RESULT offer 1: ok=#{ok} selfA=#{c7_selfsw('Sweetrot Vendor').inspect} #{c7_state} frames=#{f}")
      # --- the Gym's door is shut before Wick
      c7_shots(false)
      ok, f = c7_walk(37, 30, :touch)
      c7_run(120) { c7_idle? }
      log("RESULT gym door (step #{$game_variables[127]}): ok=#{ok} #{c7_state} frames=#{f}")
      c7_fail("the Gym door let the player in at CH7_STEP #{$game_variables[127]}") if $game_map.map_id != 220
      # --- 223: the Quiet Ward
      ok, f = c7_walk(31, 11, :touch)
      c7_shots(true)
      f = c7_run(8000) { $game_map.map_id == 223 && $game_variables[127] >= 2 && c7_idle? }
      log("RESULT quiet ward: #{c7_state} frames=#{f}")
      c7_fail("The Quiet Ward did not reach 2") if $game_variables[127] < 2
      # --- Juno: R.A. -> J2 -> the ledger
      ok, f = c7_walk(19, 13, :use)
      f2 = c7_run(4000) { $game_variables[127] >= 3 && c7_idle? }
      log("RESULT R.A. + J2: ok=#{ok} ch7_ledger=#{pf_choice(:ch7_ledger).inspect} bond=#{(Prismfall::Bonds.get(:JUNO) rescue (pf_bond(:JUNO) rescue '?'))} " \
          "battles=#{Ch7Cap.battles.inspect} #{c7_state} frames=#{f + f2}")
      c7_fail("J2 did not reach 3 / S118") if $game_variables[127] < 3 || !$game_switches[118]
      # --- out to 220: offer 2 walks up the walkway
      c7_goto(220, 31, 12, 2)
      f = c7_run(3000) { c7_selfsw("Offer 2 (walkway)") && c7_idle? }
      log("RESULT offer 2: selfA=#{c7_selfsw('Offer 2 (walkway)').inspect} #{c7_state} frames=#{f}")
      c7_fail("offer 2 did not play") if !c7_selfsw("Offer 2 (walkway)")
      # --- 648 the Weeping Fen is not built: Wick by hand
      $game_variables[127] = 4; $game_switches[119] = true; $game_map.need_refresh = true
      log("RESULT by hand: V127 3 -> 4, S119 (648 the Weeping Fen is not built)")
      # --- 223: Invoice
      c7_goto(223, 12, 17, 8)
      f = c7_run(4000) { c7_selfsw("Invoice") && c7_idle? }
      log("RESULT invoice: selfA=#{c7_selfsw('Invoice').inspect} story_items=#{(PrismfallMaps.flags[:story_items] rescue nil).inspect} #{c7_state} frames=#{f}")
      c7_fail("Invoice did not play") if !c7_selfsw("Invoice")
      # --- 220: offer 3 at the Center steps
      c7_goto(220, 10, 19, 8)
      ok, f = c7_walk(10, 17, :use)
      $game_player.turn_down                           # away from her: the plan's USE presses must not talk again
      log("RESULT offer 3: ok=#{ok} #{c7_state} frames=#{f}")
      c7_fail("offer 3 was taken (V128 #{$game_variables[128]})") if $game_variables[128] > 2
      c7_second_half(t0)
    end

    def c7_second_half(t0)
      # --- Gym 6, walked (mapgen/puzzles/infirmary.py's route)
      c7_shots(false)
      Ch7Cap.gym = true
      n0 = Ch7Cap.battles.length
      c7_goto(220, 37, 31, 8)
      c7_g6("the door", 220, 37, 29, :touch, [], 230)
      c7_g6("230 bench: fill 3", 230, 6, 9, :use, [0, 6])
      c7_g6("230 funnel <- 3", 230, 14, 9, :use, [0])
      c7_g6("230 up", 230, 10, 4, :touch, [], 231)
      c7_g6("231 bench: 5>3 tip 5>3 fill 5>3", 231, 7, 14, :use, [1, 3, 4, 3, 1, 3, 6])
      c7_g6("231 funnel <- 5 (4)", 231, 14, 10, :use, [1])
      c7_g6("231 up", 231, 14, 4, :touch, [], 232)
      c7_g6("232 bench: 1 in the 3, 5 full", 232, 3, 10, :use, [0, 2, 0, 2, 6])
      c7_g6("232 cross 1, socket A <- 3", 232, 13, 10, :use, [0])
      c7_g6("232 island refill", 232, 13, 16, :use)
      c7_g6("232 tray A: 5>3", 232, 15, 10, :use, [1, 4])
      c7_g6("232 cross 2, basin B <- 5 (2)", 232, 25, 10, :use, [1])
      c7_g6("232 back west (the fumes)", 232, 3, 10, :use, [1, 6])
      c7_g6("232 cross 1, island refill", 232, 13, 16, :use)
      c7_g6("232 cross 2, basin B <- 5 (7)", 232, 25, 10, :use, [1])
      c7_g6("232 the arena bridge", 232, 14, 4, :touch, [], 233)
      c7_shots(true)
      c7_g6("Corvin", 233, 10, 5, :use)
      f = c7_run(1200) { c7_idle? && $game_variables[127] >= 5 }
      Ch7Cap.gym = false
      log("RESULT gym 6: badge6=#{$player.badges[5].inspect} TM84=#{$bag.quantity(:TM84)} battles=#{Ch7Cap.battles[n0..-1].inspect} " \
          "#{c7_state} frames=#{f}")
      c7_fail("Gym 6 did not end on CH7_STEP 5 with the badge") if $game_variables[127] < 5 || !$player.badges[5]
      c7_ward(t0)
    end

    def c7_ward(t0)
      # --- 220: the Ward Night, then the close
      c7_goto(220, 31, 14, 8)
      ok, f = c7_walk(31, 12, :touch)
      f2 = c7_run(20000) { $game_variables[127] >= 7 && $game_map.map_id == 220 && c7_idle? }
      log("RESULT ward night + close: ward_night=#{pfm_get(:ch7_ward_night).inspect} STORY_CHAPTER=#{$game_variables[102]} " \
          "quest=#{($PokemonGlobal.pf_quests[:eighteen_roads] rescue nil).inspect} story_items=#{(PrismfallMaps.flags[:story_items] rescue nil).inspect} " \
          "#{c7_state} frames=#{f + f2} secs=#{(System.uptime - t0).round(1)}")
      c7_fail("the chapter did not close (V127 #{$game_variables[127]})") if $game_variables[127] < 7 || $game_variables[102] != 8
      c7_run(60, 60) { true }
      self.auto = false
      stop
      log("done")
    end
  end
  # every change of CH7_STEP as it happens (which map, which event)
  module Graphics
    @c7_step = nil
    @c7_tick = 0
    class << self
      alias c7_update update unless method_defined?(:c7_update)
      def update
        c7_update
        @c7_tick += 1
        if $game_variables && DemoRun.started && $game_variables[127] != @c7_step
          DemoRun.log("RESULT step #{@c7_step.inspect} -> #{$game_variables[127]} on map #{$game_map&.map_id} " \
                      "(event #{$game_system.map_interpreter.instance_variable_get(:@event_id) rescue '?'})") if !@c7_step.nil?
          @c7_step = $game_variables[127]
        end
        return if @c7_tick % 900 != 0 || !DemoRun.started
        it = $game_system.map_interpreter
        DemoRun.log("tick #{@c7_tick} map=#{$game_map&.map_id} pos=#{$game_player&.x},#{$game_player&.y} run=#{it.running?} " \
                    "ev=#{it.instance_variable_get(:@event_id)} idx=#{it.instance_variable_get(:@index)} msg=#{$game_temp.message_window_showing} " \
                    "battle=#{$game_temp.in_battle} forcing=#{$game_player.move_route_forcing}") rescue nil
      end
    end
  end
  module Input
    class << self
      alias c7_trigger? trigger? unless method_defined?(:c7_trigger?)
      def trigger?(button)
        if button == Input::USE && DemoRun.auto       # one press every 45 frames, used up by the first caller
          return false if DemoRun.frame % 45 != 0 || @c7_used == DemoRun.frame
          @c7_used = DemoRun.frame
          return true
        end
        return c7_trigger?(button)
      end
    end
  end
  alias c7_pbShowCommands pbShowCommands unless defined?(c7_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = Ch7Cap.gym ? (Ch7Cap.picks.shift || commands.length - 1) : (Ch7Cap.choices.shift || commands.length - 1)
      pick = commands.length - 1 if pick >= commands.length
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return c7_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias c7_pbCommandPhase pbCommandPhase unless method_defined?(:c7_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        DemoRun.log("battle vs #{names.join(' + ')}")
        Ch7Cap.battles << names
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      c7_pbCommandPhase
    end
  end
end
