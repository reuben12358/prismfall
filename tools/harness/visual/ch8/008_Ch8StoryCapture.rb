#===============================================================================
# Ch8 story beats on 244 / 249 / 255 in the real engine, dev tool (mapgen/layouts/story_ch8.py + cindervault.py).
#   CH8_STEP 3: 240's Foundry doors are barred -> 243: "The Hug" (-> 4, on to 244) -> "My Father" (step stays 4,
#   :gym7_open) -> 240: through the Foundry doors into Gemini's Gym 7 (layouts/cindervault_gym.py; proofs
#   puzzles/foundry.py), WALKED: 250 lever + wheel + cross -> 251 / 252 the solver's 7-move route (CH8_VAULT=1 first
#   plays the mastery vault and the Mould-Runner's reset) -> 253 Brann (LOCKED fight, auto-won; his pages are
#   story_ch8.py's) -> the Quench Badge, CH8_STEP 5, out into the square -> 240: the Five Bells
#   (-> 6) -> 249: the evacuation -> down to 255: the Caldera Crisis (6, S120, V110) -> 244: "Whose Is It"
#   (:ch8_lightstone, -> 7) -> "Chestnuts" (-> 8) -> 240: "The Herald" (-> 9, S121, V122 1) -> 243: leaving (-> 10,
#   STORY_CHAPTER 9). No step is set by hand after the start (3).
# Battles are auto-won; choices come from CH8_CHOICES (0-based, in order: the hug, Sigrun, detonator, caldera branch,
# Light Stone, Larch at the door), default 1,0,1,0,1,2. No frames unless CH8_SHOTS=1 (every CH8_EVERY-th frame, default
# 30, never less; delete frames/ch8_* and captures_keep/ch8_* after). RESULT lines in demo.log; a stage that fails stops the run (FAIL).
#   cp maps_out/Data/Map{240,243,244,249,250,251,252,253,255}.rxdata maps_out/Data/system_prismfall.txt /home/claude/run_intro/game/Data/
#   (with the lock: see .agent_brief.md; CH8_VAULT=1 CH8_SHOTS=1 CH8_EVERY=45 for the vault and sparse frames;
#   CH8_WATCHED=1 sets :ashkaar_watched first and talks to 240's oath-guard escort)
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch8/008_Ch8StoryCapture.rb --plan ch8story
# The switch / variable names Essentials needs for switch page conditions (S120 on 244) are what the Debug menu's
# "Install Prismfall maps" writes into System.rxdata; this plan puts them into $data_system in memory only.
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch8story")
  module Ch8Cap
    @choices = (ENV["CH8_CHOICES"] || "1,0,1,0,1,2").split(",").map(&:to_i)
    @battles = []
    @gym = false          # in the Foundry: every prompt takes the next of @g7 (set per action), else its last option
    @g7 = []
    class << self; attr_accessor :choices, :battles, :gym, :g7; end
  end
  class << DemoRun
    def c8_run(limit, min = 30)
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

    def c8_idle?; return !$game_system.map_interpreter.running? && !$game_temp.player_transferring && !$game_player.moving?; end

    def c8_fail(msg)
      log("FAIL #{msg}")
      self.auto = false
      stop
      log("done")
      exit
    end

    def c8_goto(map, x, y, dir)
      $game_temp.player_new_map_id = map; $game_temp.player_new_x = x; $game_temp.player_new_y = y
      $game_temp.player_new_direction = dir; $game_temp.player_transferring = true
      c8_run(300, 5) { $game_map.map_id == map && !$game_temp.player_transferring }
    end

    def c8_busy?
      return $game_system.map_interpreter.running? || $game_temp.player_transferring || $game_player.moving? ||
             $game_player.move_route_forcing || $game_temp.message_window_showing || $game_temp.in_battle ||
             $game_map.events.values.any?(&:starting)
    end

    C8_DIRS = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }

    # the first step toward a tile next to (tx, ty), going round every event tile but the trench / mould bridges
    # (Gemini's "X1 12,17", "M2 14,11", "Teach X 10,10": their own pages decide whether they can be walked)
    # (no stepping on a hatch, chute or warp on the way); 0 = there already, nil = no way
    def c8_route(tx, ty)
      blocked = {}
      $game_map.events.each_value do |e|
        next if e.name =~ /\A([XM]\d|Trench|Teach X) / || (e.x == tx && e.y == ty)
        blocked[[e.x, e.y]] = true
      end
      start = [$game_player.x, $game_player.y]
      near = ->(c) { (c[0] - tx).abs + (c[1] - ty).abs == 1 }
      return 0 if near.call(start)
      first = { start => nil }
      q = [start]
      until q.empty?
        c = q.shift
        C8_DIRS.each do |d, (dx, dy)|
          n = [c[0] + dx, c[1] + dy]
          next if first.key?(n) || blocked[n] || !$game_player.passable?(c[0], c[1], d)
          first[n] = first[c] || d
          return first[n] if near.call(n)
          q << n
        end
      end
      return nil
    end

    # walk to (tx, ty) and use it (:use: face it, the plan presses USE every 45 frames) or walk into it (:touch);
    # picks = the answers to its prompts. Trainers on the way are fought (auto-won). -> [ok, frames]
    def c8_walk(tx, ty, how = :use, picks = [], limit = 4000)
      map0 = $game_map.map_id
      tev = $game_map.events.values.find { |e| e.x == tx && e.y == ty }
      Ch8Cap.g7 = picks.dup            # already now: a target that starts by itself still gets its answers
      f = 0; stuck = 0; acting = false; seen = false
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        return [false, f] if f > limit
        busy = c8_busy?
        # the target already started on its own: the plan's USE press (every 45 frames) as the player stepped up facing
        # it (253: the causeway runs straight up to Brann), or a touch tile walked onto. The player's update marks it
        # `starting` after the interpreter has run, so it is still marked here; the interpreter takes it next frame.
        if busy && !acting && tev && $game_map.map_id == map0 &&
           (tev.starting || $game_system.map_interpreter.instance_variable_get(:@event_id) == tev.id)
          acting = true
        end
        seen = true if busy && acting
        next if busy
        if acting
          next if !seen && $game_map.map_id == map0
          Ch8Cap.g7 = []
          return [true, f]
        end
        d = c8_route(tx, ty)
        if d.nil?
          stuck += 1
          return [false, f] if stuck > 90
          next
        end
        stuck = 0
        if d == 0
          dx, dy = tx - $game_player.x, ty - $game_player.y
          dir = (dx > 0) ? 6 : (dx < 0) ? 4 : (dy > 0) ? 2 : 8
          Ch8Cap.g7 = picks.dup
          acting = true
          if how == :touch
            $game_player.move_generic(dir)      # onto it, or a bump: either way its touch page runs
          else
            $game_player.turn_generic(dir)
          end
          next
        end
        $game_player.move_generic(d)
      end
    end

    def c8_g7_state
      x = [435, 436, 437].map { |i| $game_variables[i] }
      m = [435, 436, 437].map { |i| $game_switches[i] ? 1 : 0 }
      k = [335, 336, 337].map { |i| $game_switches[i] ? 1 : 0 }
      a = [335, 336, 337].map { |i| $game_variables[i] }
      return "map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} X=#{x.join} M=#{m.join} poured=#{k.join} aims=#{a.join} " \
             "quenched=#{$game_variables[338]} teach=#{$game_variables[339]} vault=#{$game_switches[339]}"
    end

    # one gym step: walk, act, log, fail unless it ends on map `want`
    def c8_g7(label, map, tx, ty, how, picks = [], want = nil)
      c8_fail("#{label}: on map #{$game_map.map_id}, not #{map}") if $game_map.map_id != map
      ok, f = c8_walk(tx, ty, how, picks)
      log("RESULT g7 #{label}: ok=#{ok} #{c8_g7_state} frames=#{f}")
      c8_fail("#{label} did not finish") if !ok
      c8_fail("#{label}: ended on map #{$game_map.map_id}, not #{want}") if want && $game_map.map_id != want
    end

    def c8_selfsw(name, ch = "A")
      ev = $game_map.events.values.find { |e| e.name == name }
      return nil if !ev
      return $game_self_switches[[$game_map.map_id, ev.id, ch]]
    end

    def c8_names
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

    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch8 story capture boot ok; choices #{Ch8Cap.choices.inspect}")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      c8_names
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 45, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 45, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      $game_variables[129] = 3
      pfm_set(:ashkaar_watched) if ENV["CH8_WATCHED"] == "1"   # what 652's oath-gate (not built) sets on "(Say nothing.)"
      $game_map.setup(240)                             # the square first: the Foundry's doors at CH8_STEP 3
      $game_player.moveto(21, 3); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = [(ENV["CH8_EVERY"] || 30).to_i, 30].max
      record("ch8_story") if ENV["CH8_SHOTS"] == "1"
      self.auto = true
      t0 = System.uptime
      # --- CH8_STEP 3: the Foundry's doors on 240 are still barred
      ok, f = c8_walk(21, 2, :touch)
      log("RESULT foundry doors (step 3): ok=#{ok} map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} frames=#{f}")
      c8_fail("the Foundry's doors let the player in at CH8_STEP 3") if $game_map.map_id != 240
      c8_goto(243, 20, 19, 8)
      # --- "The Hug" (243) -> 244, then "My Father"
      f = c8_run(5000) { $game_map.map_id == 244 && $game_variables[129] >= 4 }
      log("RESULT the hug: CH8_STEP=#{$game_variables[129]} map=#{$game_map.map_id} frames=#{f}")
      c8_fail("The Hug did not reach 244") if $game_map.map_id != 244
      f = c8_run(5000) { c8_selfsw("My Father") && c8_idle? }
      log("RESULT my father: CH8_STEP=#{$game_variables[129]} selfA=#{c8_selfsw('My Father').inspect} gym7_open=#{pfm_get(:gym7_open).inspect} " \
          "pos=#{$game_player.x},#{$game_player.y} brann_opacity=#{$game_map.events.values.find { |e| e.name == 'Brann' }&.opacity} frames=#{f}")
      c8_fail("My Father did not finish") if !c8_selfsw("My Father") || $game_variables[129] != 4
      if ENV["CH8_WATCHED"] == "1"        # the oath-guard who keeps a PC that said nothing company (story_ch8.py)
        c8_goto(240, 31, 37, 2)
        c8_run(90, 90) { false }
        esc = $game_map.events.values.find { |e| e.name == "Oath-Guard (escort)" }
        ok, f = c8_walk(31, 38, :use)
        log("RESULT escort: selfA=#{c8_selfsw('Oath-Guard (escort)').inspect} sprite=#{esc&.character_name.inspect} ok=#{ok} frames=#{f}")
        c8_fail("the :ashkaar_watched escort did not show") if !c8_selfsw("Oath-Guard (escort)") || esc.character_name.to_s.empty?
      end
      # --- up to the square and through the Foundry's doors: Gemini's Gym 7, walked (layouts/cindervault_gym.py; the
      # route is puzzles/foundry.py's 7-move solution). Gemini's crucible menu is [Aim at the other / Pour / Leave] and
      # ends after an aim; its chutes ask "Drop down?" (Yes = 0).
      c8_goto(240, 21, 3, 8)
      Ch8Cap.gym = true
      n0 = Ch8Cap.battles.length
      c8_g7("the doors", 240, 21, 2, :touch, [], 250)
      log("RESULT 250 arrival: pos=#{$game_player.x},#{$game_player.y} dir=#{$game_player.direction} " \
          "passable_up=#{$game_player.passable?($game_player.x, $game_player.y, 8)}")
      c8_fail("250 arrival is not (12, 22)") if [$game_player.x, $game_player.y] != [12, 22]
      c8_g7("250 pour (lever)", 250, 7, 13, :use)
      c8_g7("250 quench (wheel)", 250, 17, 13, :use)
      c8_g7("250 up to the Pour Floor", 250, 12, 4, :touch, [], 251)
      if ENV["CH8_VAULT"] == "1"            # the mastery: leave X2 molten too, C1 casts M2, the hoard; the Mould-Runner resets
        c8_g7("vault: pour K1", 251, 5, 19, :use, [1])
        c8_g7("vault: pour K2", 251, 8, 19, :use, [1])
        c8_g7("vault: chute C1", 251, 14, 22, :touch, [0], 252)
        c8_g7("vault: the cracked-mould hoard", 252, 10, 8, :use)
        c8_g7("vault: the Mould-Runner's reset", 252, 18, 22, :use, [0], 251)
      end
      c8_g7("pour K1 (X1)", 251, 5, 19, :use, [1])
      c8_g7("pour K2 (X2)", 251, 8, 19, :use, [1])
      c8_g7("quench X2 (Q2)", 251, 22, 20, :use)
      c8_g7("aim K3 (X3)", 251, 11, 19, :use, [0])
      c8_g7("pour K3 (X3)", 251, 11, 19, :use, [1])
      c8_g7("chute C1", 251, 14, 22, :touch, [0], 252)
      c8_g7("ladder H up", 252, 5, 14, :touch, [], 251)
      c8_g7("chute C2", 251, 23, 8, :touch, [0], 252)
      c8_g7("north ladder up", 252, 23, 3, :touch, [], 251)
      c8_g7("up to the arena", 251, 14, 2, :touch, [], 253)
      c8_g7("Brann", 253, 10, 6, :use)
      f = c8_run(600) { c8_idle? && $game_map.map_id == 240 && $game_variables[129] >= 5 }
      Ch8Cap.gym = false
      log("RESULT gym 7: CH8_STEP=#{$game_variables[129]} badge7=#{$player.badges[6].inspect} TM35=#{$bag.quantity(:TM35)} " \
          "ELEMENTALSEED=#{$bag.quantity(:ELEMENTALSEED)} CHARCOAL=#{$bag.quantity(:CHARCOAL)} vault=#{$game_switches[339]} " \
          "battles=#{Ch8Cap.battles[n0..-1].inspect} quest=#{($PokemonGlobal.pf_quests[:eighteen_roads] rescue nil).inspect} " \
          "map=#{$game_map.map_id} frames=#{f}")
      c8_fail("Gym 7 did not end on CH8_STEP 5 with the badge") if $game_variables[129] < 5 || !$player.badges[6]
      c8_fail("the vault's hoard was not taken") if ENV["CH8_VAULT"] == "1" && (!$game_switches[339] || $bag.quantity(:ELEMENTALSEED) < 2)
      # --- the Five Bells in the square, then down to the Slag Ward
      f = c8_run(4000) { $game_variables[129] >= 6 && c8_idle? }
      log("RESULT five bells (240): CH8_STEP=#{$game_variables[129]} pos=#{$game_player.x},#{$game_player.y} tone=#{$game_screen.tone.red.round} frames=#{f}")
      c8_fail("the square's Five Bells did not reach 6") if $game_variables[129] < 6
      c8_goto(249, 6, 9, 6)
      f = c8_run(3000) { c8_selfsw("Five Bells (ward)") && !$game_system.map_interpreter.running? }
      c8_run(240, 240) { false }                       # let the families walk off
      gone = %w[Evacuee\ 1 Evacuee\ 2 Evacuee\ 3 Evacuating\ Mother Child\ with\ Litwick\ Jar].map do |n|
        e = $game_map.events.values.find { |x| x.name == n }
        "#{n}:#{e&.x},#{e&.y},o#{e&.opacity}"
      end
      log("RESULT five bells: selfA=#{c8_selfsw('Five Bells (ward)').inspect} tone=#{$game_screen.tone.red.round} evacuees=#{gone.inspect} frames=#{f}")
      c8_fail("the ward's Five Bells did not play") if !c8_selfsw("Five Bells (ward)")
      # --- down the tap stair: the crisis, then 244
      c8_goto(255, 13, 18, 8)
      f = c8_run(12000) { $game_variables[129] >= 7 && $game_map.map_id == 244 }
      log("RESULT crisis+lightstone: CH8_STEP=#{$game_variables[129]} S120=#{$game_switches[120]} V110=#{$game_variables[110]} " \
          "ch8_caldera=#{pf_choice(:ch8_caldera).inspect} ch8_lightstone=#{pf_choice(:ch8_lightstone).inspect} map=#{$game_map.map_id} " \
          "battles=#{Ch8Cap.battles.inspect} frames=#{f}")
      c8_fail("never reached CH8_STEP 7 on 244") if $game_variables[129] < 7
      # --- "Chestnuts"
      f = c8_run(6000) { $game_variables[129] >= 8 && c8_idle? && $game_screen.tone.red > -100 }
      left = $game_map.events.values.select { |e| e.character_name.to_s != "" && e.opacity > 0 }.map(&:name)
      log("RESULT chestnuts: CH8_STEP=#{$game_variables[129]} map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} " \
          "tone=#{$game_screen.tone.red.round} shown=#{left.inspect} frames=#{f}")
      # --- next morning: up to the square, "The Herald"; then out through the gate
      c8_goto(240, 20, 26, 8)
      f = c8_run(6000) { $game_variables[129] >= 9 && c8_idle? }
      log("RESULT herald: CH8_STEP=#{$game_variables[129]} S121=#{$game_switches[121]} V122=#{$game_variables[122]} " \
          "column=#{%w[Herald Standard-bearer].map { |n| e = $game_map.events.values.find { |x| x.name == n }; "#{n}:#{e&.x},#{e&.y},o#{e&.opacity}" }.inspect} frames=#{f}")
      c8_fail("The Herald did not reach 9") if $game_variables[129] < 9
      c8_goto(243, 34, 6, 2)
      f = c8_run(3000) { $game_variables[129] >= 10 && c8_idle? }
      log("RESULT leaving: CH8_STEP=#{$game_variables[129]} STORY_CHAPTER=#{$game_variables[102]} quest=#{($PokemonGlobal.pf_quests[:eighteen_roads] rescue nil).inspect} " \
          "frames=#{f} secs=#{(System.uptime - t0).round(1)}")
      c8_run(60, 60) { true }
      self.auto = false
      stop
      log("done")
    end
  end
  # every change of CH8_STEP as it happens (which map, which event), and in the gym a heartbeat every 600 frames with
  # where the frame came from (finds a stuck wait)
  module Graphics
    @c8_tick = 0
    @c8_step = nil
    class << self
      alias c8_update update unless method_defined?(:c8_update)
      def update
        c8_update
        @c8_tick += 1
        if $game_variables && DemoRun.started && $game_variables[129] != @c8_step
          DemoRun.log("RESULT step #{@c8_step.inspect} -> #{$game_variables[129]} on map #{$game_map&.map_id} " \
                      "(event #{$game_system.map_interpreter.instance_variable_get(:@event_id) rescue '?'})") if !@c8_step.nil?
          @c8_step = $game_variables[129]
        end
        return if !Ch8Cap.gym || @c8_tick % 600 != 0
        it = $game_system.map_interpreter
        DemoRun.log("tick #{@c8_tick} map=#{$game_map&.map_id} pos=#{$game_player&.x},#{$game_player&.y} run=#{it.running?} " \
                    "ev=#{it.instance_variable_get(:@event_id)} idx=#{it.instance_variable_get(:@index)} msg=#{$game_temp.message_window_showing} " \
                    "battle=#{$game_temp.in_battle} forcing=#{$game_player.move_route_forcing} moving=#{$game_player.moving?} " \
                    "at=#{caller(1, 8).map { |c| c.sub(/^.*\//, '')[0, 60] }.join(' < ')}") rescue nil
      end
    end
  end
  module Input
    class << self
      alias c8_trigger? trigger? unless method_defined?(:c8_trigger?)
      def trigger?(button)
        if button == Input::USE && DemoRun.auto       # one press every 45 frames, used up by the first caller:
          return false if DemoRun.frame % 45 != 0 || @c8_used == DemoRun.frame   # the press that closes a message
          @c8_used = DemoRun.frame                                               # mustn't also re-open the event in
          return true                                                            # front of the player that frame
        end
        return c8_trigger?(button)
      end
    end
  end
  alias c8_pbShowCommands pbShowCommands unless defined?(c8_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = Ch8Cap.gym ? (Ch8Cap.g7.shift || commands.length - 1) : (Ch8Cap.choices.shift || 0)
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return c8_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias c8_pbCommandPhase pbCommandPhase unless method_defined?(:c8_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        DemoRun.log("battle vs #{names.join(' + ')}")
        Ch8Cap.battles << names
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      c8_pbCommandPhase
    end
  end
end
