#===============================================================================
# Ch6 "What the Sand Keeps" in the real engine, dev tool (mapgen/layouts/story_ch6.py on Gemini's maps).
#   CH6_STEP 0: 608 the Act II opener (autorun) -> Dex's glass warms -> Marlo -> 180: the Mainline refuses at step 0
#   (the porter) -> 608: Juno's goodbye (-> 1) -> 180's west avenue -> 612: The Checkpoint (-> 2) -> 203: the Sandgate
#   (-> 3) -> 200: the Dig's door is shut at 3 -> 209: Sahar (first meeting) -> 204: The Deep-works, :ch6_drillsite
#   (-> 4) -> 200: the Dig's door -> Gym 5 WALKED on the solver's route (puzzles/dig.py: the entrance drop, lane c,
#   M2 twice, lane b, then lanes a and c up to the stair) -> 213 Sahar (auto-won; badge, TM83, -> 5) -> 210 the
#   excavators (HM04) -> 620: The Door in the Skull (-> 6) -> 624: the Ossuary, the four murals, the rubbing (-> 7)
#   -> 620: Lecture, Archaeological + K3 (-> 8) -> Juno's letter (-> 9, STORY_CHAPTER 7).
# Hand transfers (c6_goto) only: 612 -> 203 (the road 600 / 610 / 601 / 613 is not walked; its links are checked in
# the specs), into Duneholt's maps, and 210 -> 620. No CH6_STEP is ever set by hand after the start (0): 602 and 603
# are unbuilt but no step lives on them.
# Battles are auto-won; choices from CH6_CHOICES (0-based, in order: Juno, the drill site, Sahar's joke, Kestrel),
# default 0,2,1,0 (:sanctuary, :encourage). Gym prompts take the per-step picks. No frames unless CH6_SHOTS=1 (every
# 30th; delete frames/ch6_* and captures_keep/ch6_* after). RESULT lines in demo.log; a failed stage stops (FAIL).
#   cp maps_out/Data/Map{180,200,201,203,204,209,210,211,212,213,608,612,620,624}.rxdata maps_out/Data/system_prismfall.txt \
#      maps_out/Data/mapinfos_prismfall.txt /home/claude/run_intro/game/Data/
#   bash tools/harness/visual/intro/run_intro.sh --capture $PWD/tools/harness/visual/ch6/010_Ch6StoryCapture.rb --plan ch6story
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch6story")
  module Ch6Cap
    @choices = (ENV["CH6_CHOICES"] || "0,2,1,0").split(",").map(&:to_i)
    @battles = []
    @gym = false          # in the Dig: every prompt takes the next of @g5 (set per action), else its last option
    @g5 = []
    class << self; attr_accessor :choices, :battles, :gym, :g5; end
  end
  class << DemoRun
    # with CH6_SHOTS=1, every RESULT line also says which frame file was being written (for picking a beat's frames)
    alias c6_log0 log unless method_defined?(:c6_log0)
    def log(msg); c6_log0((@rec && msg.to_s.start_with?("RESULT")) ? "#{msg} shot=#{@shots}" : msg); end

    def c6_run(limit, min = 30)
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

    def c6_idle?; return !$game_system.map_interpreter.running? && !$game_temp.player_transferring && !$game_player.moving?; end

    def c6_fail(msg)
      log("FAIL #{msg}")
      self.auto = false
      stop
      log("done")
      exit
    end

    def c6_goto(map, x, y, dir)
      $game_temp.player_new_map_id = map; $game_temp.player_new_x = x; $game_temp.player_new_y = y
      $game_temp.player_new_direction = dir; $game_temp.player_transferring = true
      c6_run(300, 5) { $game_map.map_id == map && !$game_temp.player_transferring }
    end

    def c6_busy?
      return $game_system.map_interpreter.running? || $game_temp.player_transferring || $game_player.moving? ||
             $game_player.move_route_forcing || $game_temp.message_window_showing || $game_temp.in_battle ||
             $game_map.events.values.any?(&:starting)
    end

    C6_DIRS = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }

    # the first step toward a tile next to (tx, ty) going round every event tile, except the Dig's lanes while their
    # page is crust (a touch page is soft sand: never walked by accident); 0 = there already, nil = no way
    def c6_route(tx, ty)
      blocked = {}
      $game_map.events.each_value do |e|
        next if e.x == tx && e.y == ty
        next if e.name.start_with?("Sand ") && e.trigger != 1
        next if e.through && e.character_name.to_s == "" && e.trigger != 1 && e.trigger != 2 && !e.name.start_with?("Teach")
        blocked[[e.x, e.y]] = true
      end
      start = [$game_player.x, $game_player.y]
      near = ->(c) { (c[0] - tx).abs + (c[1] - ty).abs == 1 }
      return 0 if near.call(start)
      first = { start => nil }
      q = [start]
      until q.empty?
        c = q.shift
        C6_DIRS.each do |d, (dx, dy)|
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
    def c6_walk(tx, ty, how = :use, picks = [], limit = 5000)
      map0 = $game_map.map_id
      f = 0; stuck = 0; acting = false; seen = false
      loop do
        Graphics.update; Input.update
        $scene.update
        f += 1
        return [false, f] if f > limit
        busy = c6_busy?
        seen = true if busy && acting
        next if busy
        if acting
          next if !seen && $game_map.map_id == map0
          Ch6Cap.g5 = []
          return [true, f]
        end
        d = c6_route(tx, ty)
        if d.nil?
          stuck += 1
          return [false, f] if stuck > 90
          next
        end
        stuck = 0
        if d == 0
          dx, dy = tx - $game_player.x, ty - $game_player.y
          dir = (dx > 0) ? 6 : (dx < 0) ? 4 : (dy > 0) ? 2 : 8
          Ch6Cap.g5 = picks.dup
          acting = true
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

    def c6_state
      return "map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} CH6_STEP=#{$game_variables[126]} " \
             "V325=#{$game_variables[325]} V326=#{$game_variables[326]}"
    end

    # one walked step: fail unless it ends on map `want`
    def c6_step(label, map, tx, ty, how, picks = [], want = nil)
      c6_fail("#{label}: on map #{$game_map.map_id}, not #{map}") if $game_map.map_id != map
      ok, f = c6_walk(tx, ty, how, picks)
      log("RESULT #{label}: ok=#{ok} #{c6_state} frames=#{f}")
      c6_fail("#{label} did not finish") if !ok
      c6_fail("#{label}: ended on map #{$game_map.map_id}, not #{want}") if want && $game_map.map_id != want
    end

    def c6_wait_step(n, label, limit = 6000)
      f = c6_run(limit) { $game_variables[126] >= n && c6_idle? }
      log("RESULT #{label}: #{c6_state} frames=#{f}")
      c6_fail("#{label} never reached CH6_STEP #{n}") if $game_variables[126] < n
    end

    def c6_selfsw(name, ch = "A")
      ev = $game_map.events.values.find { |e| e.name == name }
      return nil if !ev
      return $game_self_switches[[$game_map.map_id, ev.id, ch]]
    end

    def c6_names
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
      log("ch6 story capture boot ok; choices #{Ch6Cap.choices.inspect}")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      c6_names
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 31, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 31, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      4.times { |i| $player.badges[i] = true }
      # the chapter start (Interlude I's end): STORY_ACT 2, STORY_CHAPTER 6, CH5_STEP 13, the Lowlight shattered, Mandate on
      $game_variables[101] = 2; $game_variables[102] = 6; $game_variables[125] = 13; $game_variables[104] = 1
      $game_switches[113] = $game_switches[114] = $game_switches[115] = true
      $game_variables[126] = 0
      $game_map.setup(608)
      ev = $game_map.events.values.find { |e| e.name == "Aftermath" }    # Ch5's 608 autorun played long ago
      $game_self_switches[[608, ev.id, "A"]] = true if ev
      $game_player.moveto(1, 8); $game_player.turn_right
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = 30
      record("ch6_story") if ENV["CH6_SHOTS"] == "1"
      self.auto = true
      t0 = System.uptime
      # --- 608: the opener plays by itself
      f = c6_run(4000) { c6_selfsw("Act II Opener") && c6_idle? }
      log("RESULT opener: selfA=#{c6_selfsw('Act II Opener').inspect} #{c6_state} tone=#{$game_screen.tone.red.round} frames=#{f}")
      c6_fail("the Act II opener did not play") if !c6_selfsw("Act II Opener")
      c6_step("Dex's glass", 608, 4, 7, :use)
      log("RESULT dex: warm_played=#{c6_selfsw('Glass Dex').inspect}")
      c6_step("Marlo", 608, 1, 9, :use)
      # --- 180 at step 0: the Mainline sends you back (the porter)
      c6_goto(180, 1, 34, 4)
      c6_step("Mainline at step 0", 180, 0, 34, :touch)
      c6_fail("the Mainline let the player out at CH6_STEP 0") if $game_map.map_id != 180
      # --- 608: Juno's goodbye
      c6_goto(608, 2, 8, 8)
      c6_step("Juno's goodbye", 608, 1, 7, :use)
      c6_wait_step(1, "goodbye")
      log("RESULT quest: #{($PokemonGlobal.pf_quests[:ch6_eighteen_roads] rescue nil).inspect}")
      # --- 180 -> 612: the Checkpoint
      c6_goto(180, 1, 34, 4)
      c6_step("the Mainline", 180, 0, 34, :touch, [], 612)
      c6_wait_step(2, "the checkpoint")
      log("RESULT barrier: S576=#{$game_switches[576]} testimony=#{(pf_choice(:ch5_lowlight_testimony) rescue nil).inspect}")
      # --- 203 the Sandgate
      c6_goto(203, 19, 21, 8)
      c6_wait_step(3, "the sandgate")
      # --- 200: the Dig is shut before the drill site
      c6_goto(200, 8, 39, 8)
      c6_step("the Dig's door at step 3", 200, 8, 38, :touch)
      c6_fail("the Dig let the player in at CH6_STEP 3") if $game_map.map_id != 200
      # --- 209 Sahar, then 204 the Deep-works
      c6_goto(209, 10, 13, 8)
      c6_step("Sahar (first meeting)", 209, 10, 5, :use)
      log("RESULT sahar: met=#{pfm_get(:ch6_met_sahar).inspect} selfA=#{c6_selfsw('Sahar').inspect}")
      c6_goto(204, 1, 17, 6)
      c6_wait_step(4, "the deep-works", 9000)
      log("RESULT drillsite: #{(pf_choice(:ch6_drillsite) rescue nil).inspect} battles=#{Ch6Cap.battles.inspect} " \
          "mandate_pass=#{(pfm_has?(:MANDATEPASS) rescue nil).inspect}")
      # --- Gym 5, walked (puzzles/dig.py)
      c6_goto(200, 8, 39, 8)
      Ch6Cap.gym = true
      n0 = Ch6Cap.battles.length
      c6_step("the Dig's door", 200, 8, 38, :touch, [], 210)
      c6_step("210 the entrance drop", 210, 10, 9, :touch, [], 212)
      c6_step("212 the cellar ladder", 212, 14, 22, :touch, [], 211)
      c6_step("211 drop into lane c", 211, 5, 8, :touch, [], 212)
      c6_step("212 ladder Hc", 212, 22, 12, :touch, [], 211)
      c6_step("211 M2 (1)", 211, 25, 12, :use, [0])
      c6_step("211 M2 (2)", 211, 25, 12, :use, [0])
      c6_step("211 drop into lane b", 211, 22, 20, :touch, [], 212)
      c6_step("212 ladder Hb", 212, 18, 20, :touch, [], 211)
      c6_step("211 up to the arena", 211, 14, 2, :touch, [], 213)
      c6_step("Sahar", 213, 10, 4, :use)
      f = c6_run(900) { c6_idle? && $game_variables[126] >= 5 }
      Ch6Cap.gym = false
      log("RESULT gym 5: #{c6_state} badge5=#{$player.badges[4].inspect} TM83=#{$bag.quantity(:TM83)} " \
          "battles=#{Ch6Cap.battles[n0..-1].inspect} frames=#{f}")
      c6_fail("Gym 5 did not end on CH6_STEP 5 with the badge") if $game_variables[126] < 5 || !$player.badges[4]
      c6_step("the excavators", 210, 15, 11, :use) if $game_map.map_id == 210
      log("RESULT strength: HM04=#{$bag.quantity(:HM04)}")
      # --- 620 the Door in the Skull -> 624
      c6_goto(620, 50, 36, 6)
      c6_step("the door in the skull", 620, 55, 36, :touch, [], 624)
      c6_wait_step(6, "the door")
      f = c6_run(3000) { c6_selfsw("Into the Ossuary") && c6_idle? }
      log("RESULT ossuary entry: selfA=#{c6_selfsw('Into the Ossuary').inspect} convoy=#{(pf_echo_follow(:active?) rescue nil).inspect} frames=#{f}")
      c6_step("Mural I", 624, 9, 18, :use)
      c6_step("Mural II", 624, 17, 16, :use)
      c6_step("Mural III", 624, 34, 18, :use)
      c6_step("Mural IV", 624, 18, 6, :use)
      c6_wait_step(7, "the rubbing")
      log("RESULT rubbing: S116=#{$game_switches[116]} item=#{(pfm_has?(:DUNEHOLTRUBBING) rescue nil).inspect}")
      # --- out: Lecture, Archaeological; K3; Juno's letter
      c6_step("out of the Ossuary", 624, 21, 38, :touch, [], 620)
      c6_wait_step(8, "K3", 9000)
      log("RESULT k3: S117=#{$game_switches[117]} rumor=#{(pf_choice(:ch6_kestrel_rumor) rescue nil).inspect} V114=#{$game_variables[114]} " \
          "battles=#{Ch6Cap.battles.inspect}")
      c6_wait_step(9, "Juno's letter")
      log("RESULT chapter close: STORY_CHAPTER=#{$game_variables[102]} quest=#{($PokemonGlobal.pf_quests[:ch6_eighteen_roads] rescue nil).inspect} " \
          "secs=#{(System.uptime - t0).round(1)}")
      c6_run(60, 60) { true }
      self.auto = false
      stop
      log("done")
    end
  end
  # every change of CH6_STEP as it happens (which map, which event); in the gym a heartbeat every 600 frames
  module Graphics
    @c6_tick = 0
    @c6_step = nil
    class << self
      alias c6_update update unless method_defined?(:c6_update)
      def update
        c6_update
        @c6_tick += 1
        if $game_variables && DemoRun.started && $game_variables[126] != @c6_step
          DemoRun.log("RESULT step #{@c6_step.inspect} -> #{$game_variables[126]} on map #{$game_map&.map_id} " \
                      "(event #{$game_system.map_interpreter.instance_variable_get(:@event_id) rescue '?'})") if !@c6_step.nil?
          @c6_step = $game_variables[126]
        end
        return if @c6_tick % 600 != 0 || !DemoRun.started
        it = $game_system.map_interpreter
        DemoRun.log("tick #{@c6_tick} map=#{$game_map&.map_id} pos=#{$game_player&.x},#{$game_player&.y} run=#{it.running?} " \
                    "ev=#{it.instance_variable_get(:@event_id)} idx=#{it.instance_variable_get(:@index)} msg=#{$game_temp.message_window_showing} " \
                    "battle=#{$game_temp.in_battle} forcing=#{$game_player.move_route_forcing} moving=#{$game_player.moving?}") rescue nil
      end
    end
  end
  module Input
    class << self
      alias c6_trigger? trigger? unless method_defined?(:c6_trigger?)
      def trigger?(button)
        if button == Input::USE && DemoRun.auto       # one press every 45 frames, used up by the first caller
          return false if DemoRun.frame % 45 != 0 || @c6_used == DemoRun.frame
          @c6_used = DemoRun.frame
          return true
        end
        return c6_trigger?(button)
      end
    end
  end
  alias c6_pbShowCommands pbShowCommands unless defined?(c6_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = Ch6Cap.gym ? (Ch6Cap.g5.shift || commands.length - 1) : (Ch6Cap.choices.shift || 0)
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return c6_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands
  class Battle
    alias c6_pbCommandPhase pbCommandPhase unless method_defined?(:c6_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}/#{t.version rescue '?'}" }
        DemoRun.log("battle vs #{names.join(' + ')}")
        Ch6Cap.battles << names
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      c6_pbCommandPhase
    end
  end
end
