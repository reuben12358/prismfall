#===============================================================================
# DEV-ONLY playtest bot. run_playtest.sh installs it into the test copy only;
# never ship it. It plays the first minutes of a New Game with ordinary input:
# - presses Use when a message has finished and waits for input,
# - picks menu and choice entries by their text (moves the cursor with Up/Down),
# - types the player's name on the on-screen keyboard,
# - walks with the arrow keys along BFS paths (Game_Player#passable?),
# - lets the AI play the player's side of battles (battle.controlPlayer),
# and saves Graphics.screenshot PNGs: key shots + every Nth frame for a GIF.
# PLAYBOT_SESSION=install  boot, New Game, accept the install offer, look, quit
# PLAYBOT_SESSION=play     New Game, Debug > Files > Install (idempotency), prologue
#===============================================================================
module PlayBot
  ROOT     = "Playtest"
  SESSION  = (ENV["PLAYBOT_SESSION"] || "play")
  NAME     = "Wren"
  REC_EVERY = (ENV["PLAYBOT_REC_EVERY"] || 6).to_i
  MAX_FRAMES = (ENV["PLAYBOT_MAX_FRAMES"] || 60_000).to_i
  B = Input   # button constants

  # [kind, map, x, y, extra]; :goto walks onto a tile, :bump walks into a blocking
  # event (doors), :talk faces a tile and presses Use, :edge holds a direction off
  # the map edge into a connected map, :debug_install runs the Debug menu entry.
  # Steps name maps by ID and targets by event name, never by coordinates (maps are still being rebuilt):
  #   [:to, map, dest]      take the transfer event or map edge that leads to map dest (doors are bumped)
  #   [:goto, map, name]    walk onto the event    [:near, map, name]  stand next to it
  #   [:talk, map, name]    face it and press Use  [:spot_all, map]    walk into every unbeaten trainer's sight
  #   [:catch, map]         walk the tall grass until a second Pokemon is caught (bot throws Poke Balls)
  PLAN = [
    [:debug_install, 109],
    [:to, 109, 110], [:talk, 110, "Mum's letter"], [:to, 110, 109],
    [:goto, 109, "Rail watch 3"], [:near, 109, "Rail watch 3"], [:goto, 109, "Rail watch 2"],   # Edda, then Voss
    [:to, 109, 100],                               # gangway -> Ferrow's Landing
    [:goto, 100, "Customs gate 2"],                # Edda's last call, the NULL scan
    [:to, 100, 103], [:talk, 103, "Starter table"], [:to, 103, 100],   # Larch, starter, K1 at the lab gate
    [:to, 100, 101], [:talk, 101, "Nurse"], [:to, 101, 100],           # Poke Center in/out (door step-out 1)
    [:to, 100, 102], [:to, 102, 100],                                  # Mart in/out (door step-out 2)
    [:to, 100, 520],
    [:goto, 520, "Juno tutorial 4"], [:catch, 520], [:spot_all, 520],
    [:to, 520, 521], [:spot_all, 521],
    [:to, 521, 522], [:talk, 522, "Glassed Wurmple"], [:talk, 522, "Lost Skwovet"], [:goto, 522, "Bleed Veil 2"],
    [:to, 522, 521],                               # "Juno flags 1" moved to the Dyers' Ford (552) in Rev 14
    [:to, 521, 523], [:talk, 523, "Wenna"], [:to, 523, 521],
    [:to, 521, 520], [:goto, 520, "Stile send-off 2"],   # the stile send-off closes Chapter 1
    # Chapter 2 (SPINE Rev 14, design/SWAP_GYM1_GYM2.md 1A): the Strand Road 520 W -> 527 -> 528 -> Saltmere 140 East
    # Gate, then Gym 1 (147 -> 150 -> 154). The forest road 521 -> 524 is corded until after Gym 2. Until map builder 9's
    # rewiring is installed, :need_map ends the run here, at the end of Chapter 1.
    [:need_map, 527],
    [:to, 520, 527], [:spot_all, 527], [:to, 527, 528], [:spot_all, 528], [:to, 528, 140], [:arrive, 140],
    [:to, 140, 141], [:talk, 141, "Nurse"], [:to, 141, 140],
    [:talk, 140, "Juno J1"],                       # J1 on the promenade green, before the gym
    [:to, 140, 147], [:arrive, 147],               # Old Town, outside the Pell Playhouse
    # Gym 1 (147 -> 150 -> 154: [:spot_all, 154], [:talk, 154, "Curtain rope"], [:talk, 154, "Dorian"]) is held back:
    # the puzzle engineer is adding crowd logic (2026-11-19), so no gym is attempted until they report.
    [:done]
  ]
  MAX_BLACKOUTS = (ENV["PLAYBOT_MAX_BLACKOUTS"] || 5).to_i
  # PLAYBOT_SESSION=route1: start on Route 1 after K1 (dev shortcut) to re-check the Route 1 trainers quickly
  ROUTE1_PLAN = [[:goto, 520, "Juno tutorial 4"], [:spot_all, 520], [:done]]
  # PLAYBOT_SESSION=checks: real map lines with glyphs the fonts lack, a quest-log line, then every trainer added on
  # 2026-11-17 (AI vs AI, two turns each) - checks 002_Font_Glyphs.rb and the new PBS entries in the engine
  CHECK_LINES = [
    "\\pf[EDDA,shocked,dots]Edda: Don't lean on my rail like that, you'll\u2014 huh.",
    "\u2191 Tidewatch Station (Prof. I. Larch) \u00b7 \u2192 Hale's Bramble \u00b7 \u2190 Lighthouse (KEEP OUT. THIS MEANS YOU, KESTREL.)",
    "The last page: \"Received of the Meridian Concord, for stewardship rights, Lattice 15: \u20bd400,000. Signed, T. Loom, Warden.\"",
    "A fierce old woman at a loom. Brass plate: \"Mother Loom, Warden AF 247\u2013299. 'Twist it or lose it.'\"",
    "Smart quotes and ellipsis are real glyphs: \u201cfine\u201d, \u2018fine\u2019\u2026"
  ]
  CHECK_TRAINERS = [[:YOUNGSTER, "Pim"], [:LASS, "Dory"], [:BUGCATCHER, "Wim"], [:PICNICKER, "Ada"], [:TWINS, "Mo & Jo", true],
                    [:BUGCATCHER, "Nell"], [:LASS, "Orla"], [:GENTLEMAN, "Bram"], [:POKEMANIAC, "Ferris"], [:LASS, "Tilde"],
                    [:SAILOR, "Haakon"], [:BIRDKEEPER, "Ailsa"], [:BUGCATCHER, "Pell"], [:POKEMONRANGER_F, "Orla"],
                    [:HIKER, "Ulf"], [:CAMPER, "Rook"], [:TWINS, "Ana & Ida", true], [:POKEMONRANGER_M, "Sigurd"]]
  CHECKS_PLAN = [[:run_checks, 520], [:done]]
  # PLAYBOT_SESSION=narrative: Debug > Prismfall Core... > Show Core status (runs Prismfall::NarrativeCheck in the engine),
  # then evaluates every condition it walks (WARDEN_CONSENT included) against the live save
  NARRATIVE_PLAN = [[:debug_install, 520], [:eval_conditions, 520], [:done]]
  DEBUG_PATH = (SESSION == "narrative") ? [/^Prismfall Core/, /^Show Core status/] : [/^Files options/, /^Install Prismfall maps/]

  @frame = 0; @armed = {}; @live = {}; @dir = 0; @step = 0; @step_start = 0; @idle = 0
  @cmd = nil; @cmd_seen = -10; @cmd_key = nil; @cmd_target = nil; @cmd_since = 0; @cmd_moved = 0
  @cmd_used = {}; @msgwin = nil; @msg_seen = -10; @msg_pause = 0; @msg_wait = 0; @last_text = ""
  @seen = {}; @nshot = 0; @nframe = 0; @recording = false; @fatal = nil; @use_tick = 0
  @map_arrival = nil; @battle_frames = 0; @debug_phase = nil; @entry = nil; @step_ran_event = false
  @last_map = nil; @ready = 0; @went_busy = 0; @typed = 0; @entry_done = false
  @spot_i = 0; @spot_wait = 0; @map_wait = 0; @talk_n = 0; @bumps = 0; @nopath = 0

  class << self
    attr_accessor :recording, :debug_phase, :battle_tag
    attr_reader :frame

    def log(msg)
      Dir.mkdir(ROOT) if !Dir.exist?(ROOT)
      File.open("#{ROOT}/bot.log", "a") { |f| f.puts(format("[%6d] %s", @frame, msg)) }
    end

    def shot(name)
      ["#{ROOT}", "#{ROOT}/shots"].each { |d| Dir.mkdir(d) if !Dir.exist?(d) }
      @nshot += 1
      file = format("%s/shots/%03d_%s.png", ROOT, @nshot, name.to_s.gsub(/[^\w\-]+/, "_")[0, 60])
      Graphics.screenshot(file)
      log("shot #{file}")
    rescue StandardError => e
      log("shot failed #{e.class}: #{e.message}")
    end

    def shot_once(key, name = key)
      return if @seen[key]
      @seen[key] = true
      shot(name)
    end

    # Like a key press: armed now, live from the next Input.update until the one after (so the Input.update
    # that pbMessageDisplay calls on closing clears it, and a press never leaks into the next screen)
    def press(button);  @armed[button] = true; end
    def pressed?(b);    return !@planning && @live.has_key?(b); end
    def input_updated;  @live = @armed; @armed = {}; end
    def dir;            return @dir; end
    def last_text=(t);  @last_text = t.to_s; end

    def saw_cmd(w);  @cmd = w; @cmd_seen = @frame; end
    def saw_msg(w);  @msgwin = w; @msg_seen = @frame; end

    def fatal(text)
      return if @fatal
      @fatal = text
      log("FATAL " + text)
      shot("FATAL")
    end

    #---------------------------------------------------------------------------
    # Called once per Graphics.update (start of a frame)
    #---------------------------------------------------------------------------
    def tick
      @frame += 1
      if @recording && REC_EVERY > 0 && @frame % REC_EVERY == 0
        Dir.mkdir("#{ROOT}/frames") if !Dir.exist?("#{ROOT}/frames")
        Graphics.screenshot(format("%s/frames/f%06d.png", ROOT, @nframe)) rescue nil
        @nframe += 1
      end
      @dir = 0
      if @fatal || @frame > MAX_FRAMES
        log(@fatal ? "exit after fatal error" : "frame limit reached at step #{@step}")
        shot("frame_limit") if !@fatal
        finish
      end
      brain
    rescue Exception => e
      raise if e.is_a?(SystemExit)
      log("bot error #{e.class}: #{e.message}\n  " + (e.backtrace || [])[0, 8].join("\n  "))
    end

    def finish
      log("bot finished (#{@nshot} shots, #{@nframe} frames)")
      Kernel.exit!(0)
    end

    def on_map?
      return $scene.is_a?(Scene_Map) && $game_map && $game_player
    end

    # Nothing but the player may be moving: no message, menu, battle, transfer or event
    def map_ready?
      return false if !on_map? || !$game_temp
      return false if $game_temp.message_window_showing || $game_temp.in_menu || $game_temp.in_battle
      return false if $game_temp.player_transferring || $game_temp.transition_processing
      return false if pbMapInterpreterRunning?
      return false if $game_temp.respond_to?(:in_mini_update) && $game_temp.in_mini_update
      return true
    end

    def busy_flags
      return "scene #{$scene.class}" if !on_map? || !$game_temp
      t = $game_temp
      return "msg=#{t.message_window_showing} menu=#{t.in_menu} battle=#{t.in_battle} xfer=#{t.player_transferring} " \
             "trans=#{t.transition_processing} mini=#{t.respond_to?(:in_mini_update) && t.in_mini_update} " \
             "interp=#{pbMapInterpreterRunning?} msgwin=#{@msgwin && !@msgwin.disposed? && @msgwin.visible}"
    end

    def map_idle?
      return map_ready? && !$game_player.moving? && !$game_player.jumping?
    end

    def brain
      @planning = true
      brain_inner
    ensure
      @planning = false
    end

    def brain_inner
      cmd_live = @cmd && @cmd_seen >= @frame - 2 && !@cmd.disposed? && @cmd.visible && @cmd.active
      msg_live = @msgwin && @msg_seen >= @frame - 2 && !@msgwin.disposed? && @msgwin.visible &&
                 ($game_temp.nil? || $game_temp.message_window_showing)
      track_map
      @battle_frames = 0 if !($game_temp && $game_temp.in_battle)
      if @entry && !@entry_done
        drive_entry
      elsif cmd_live
        drive_cmd
      elsif $game_temp && $game_temp.in_battle
        drive_battle
      elsif msg_live
        drive_msg
      elsif map_ready?
        @ready += 1
        @idle = ($game_player.moving? || $game_player.jumping?) ? 0 : @idle + 1
        drive_plan if @ready >= 12
        return
      else
        # Boot messages, load screen, cutscenes, scripted waits: Use every 30 frames is harmless here
        @use_tick += 1
        press(B::USE) if @use_tick % 30 == 0
        log("busy: " + busy_flags) if @use_tick % 600 == 0
      end
      @went_busy = @frame
      @ready = 0
      @idle = 0
    end

    def track_map
      return if !on_map?
      id = $game_map.map_id
      if id != @last_map
        log("on map #{id} #{$game_map.name rescue '?'} at (#{$game_player.x},#{$game_player.y}); party #{party_text rescue '?'}")
        @last_map = id
        @map_arrival = @frame
        @path = nil
        @map_wait = 0
      end
      age = @frame - @map_arrival
      shot("map#{id}_arrival") if age == 45
      if SESSION == "install" && age == 240
        shot("install_session_map#{id}")
        finish
      end
      if map_idle? && @idle == 30
        shot_once("map#{id}_idle", "map#{id}_#{$game_map.name rescue ''}")
      end
    end

    #---------------------------------------------------------------------------
    # Messages and choices
    #---------------------------------------------------------------------------
    def drive_msg
      w = @msgwin
      if w.respond_to?(:pausing?) && w.pausing?
        @msg_wait = 0
        @msg_pause += 1
        bubble_shot if @msg_pause == 10
        shot("msg_" + @last_text.to_s.gsub(/\\\w+\[[^\]]*\]/, "")[0, 24]) if @msg_pause == 10 && SESSION == "checks"
        if @msg_pause >= 24
          press(B::USE)
          @msg_pause = 0
        end
      else
        @msg_pause = 0
        @msg_wait += 1
        if @msg_wait >= 300          # a box that never pauses: nudge it
          press(B::USE)
          @msg_wait = 0
        end
      end
    end

    def bubble_shot
      p = (defined?(Prismfall::Portrait) && Prismfall::Portrait.respond_to?(:current)) ? Prismfall::Portrait.current : nil
      return if !p
      spec = p.instance_variable_get(:@spec) || {}
      who = spec[:id] || "unknown"
      @bubbles ||= Hash.new(0)
      @bubbles[who] += 1
      shot("bubble_#{who}_#{spec[:expression]}") if @bubbles[who] <= 2
    end

    def clean(cmd)
      return cmd.to_s.gsub(/<[^>]*>/, "").gsub(/\\c\[\d+\]/i, "").strip
    end

    def choose(cmds)
      c = cmds.map { |x| clean(x) }
      t = @last_text.to_s
      find = proc { |re| c.index { |x| x =~ re } }
      if [:opening, :open].include?(@debug_phase)
        menu, entry = DEBUG_PATH
        @debug_phase = :open if find.call(menu) || find.call(entry)
        if @debug_phase == :open
          return find.call(menu) if find.call(menu) && !@cmd_used[:files]
          return find.call(entry) if find.call(entry) && !@cmd_used[:install]
          return :back
        end
      end
      return :back if @debug_phase == :leaving
      rules = [/^New Game$/, /Style A/, /^Standard$/, /^That's right\.$/, /^Nerve\.$/, /^Thank you\.$/,
               /^I'm staying\.$/, /^Drink it\.$/, /^It said NULL\.$/, /^Generation 3$/, /^Water: /,
               /^I was born here\.$/, /^Why not\?$/, /^I'm fine\.$/, /^Who\?$/,
               /^No\. Stay there\.$/, /^It was stuck\.$/]   # never "Take her hand" (Game Over GO_ORCHARD)
      rules.each { |re| i = find.call(re); return i if i }
      if c.length == 2 && c[0] =~ /^Yes$/i && c[1] =~ /^No$/i
        return 0 if t =~ /Play on|install them now|give up|stop trying|stop learning|heal your|rest your|take a rest/i
        return 1
      end
      return nil   # keep the default cursor
    end

    def drive_cmd
      w = @cmd
      cmds = (w.respond_to?(:commands)) ? w.commands : []
      key = [w.object_id, cmds.join("|")]
      if key != @cmd_key
        @cmd_key = key
        @cmd_target = choose(cmds)
        @cmd_target = w.index if @cmd_target.nil?
        @cmd_since = @frame
        @cmd_moved = @frame
        log("choice #{cmds.map { |x| clean(x) }.inspect} (after #{@last_text[0, 60].inspect}) -> #{@cmd_target}")
      end
      age = @frame - @cmd_since
      shot_once("choice:" + cmds.join("|")[0, 80], "choice_" + clean(cmds[0])) if age == 16
      return if age < 24
      if @cmd_target == :back
        press(B::BACK) if age % 20 == 0
        return
      end
      if w.index < @cmd_target
        (press(B::DOWN); @cmd_moved = @frame) if (@frame - @cmd_moved) >= 6
      elsif w.index > @cmd_target
        (press(B::UP); @cmd_moved = @frame) if (@frame - @cmd_moved) >= 6
      elsif @frame - @cmd_moved >= 14
        label = clean(cmds[@cmd_target])
        @cmd_used[:files] = true if label =~ DEBUG_PATH[0] && @debug_phase == :open
        @cmd_used[:install] = true if label =~ DEBUG_PATH[1] && @debug_phase == :open
        press(B::USE)
        @cmd_key = nil        # look again if the same window stays (e.g. the Debug menu)
      end
    end

    # On-screen keyboard (PokemonEntryScene2): move the cursor to each letter and press Use
    def drive_entry
      sc = @entry
      @entry_start ||= @frame
      age = @frame - @entry_start
      return if age < 40
      if @typed < NAME.length
        return if age % 12 != 0
        mode = sc.instance_variable_get(:@mode)
        chars = PokemonEntryScene2.class_variable_get(:@@Characters)[mode][0]
        pos = chars.index(NAME[@typed])
        if pos.nil?                  # the page is still switching (auto-lowercase): try again, then switch it
          @entry_miss = (@entry_miss || 0) + 1
          press(B::SPECIAL) if @entry_miss % 5 == 0
          return
        end
        @entry_miss = 0
        sc.instance_variable_set(:@cursorpos, pos)
        sc.instance_variable_get(:@sprites)["cursor"].setCursorPos(pos)
        press(B::USE)
        @typed += 1
      elsif !@entry_ok
        @entry_ok = @frame if age % 12 == 0
        shot("name_entry") if @entry_ok
        press(B::ACTION) if @entry_ok   # jumps to OK
      elsif @frame - @entry_ok == 12
        press(B::USE)
        @entry_done = true
        log("typed name #{NAME}")
      end
    end

    def entry=(e)
      @entry = e
      @entry_start = nil; @typed = 0; @entry_ok = nil; @entry_done = false
    end

    def drive_battle
      @battle_frames += 1
      shot("battle_#{@battle_tag || 'start'}") if @battle_frames == 240
      shot("battle_t#{@battle_frames}") if @battle_frames > 150 && @battle_frames % 900 == 0
      press(B::USE) if @battle_frames % 20 == 0
    end

    #---------------------------------------------------------------------------
    # Plan steps (run while the map is free; walking keeps going while moving)
    #---------------------------------------------------------------------------
    def plan
      return PLAN if SESSION == "resume"
      return ROUTE1_PLAN if SESSION == "route1"
      return CHECKS_PLAN if SESSION == "checks"
      return NARRATIVE_PLAN if SESSION == "narrative"
      return PLAN[PLAN.index { |st| st[1] == 520 }..] if SESSION == "ch1"   # resume at Route 1, state as after K1
      return PLAN
    end

    # Queue the checks as an event list on the map interpreter (so messages and battles run as from a map event)
    def run_checks
      return next_step if @checks_queued
      @checks_queued = true
      cmds = CHECK_LINES.map { |t| RPG::EventCommand.new(101, 0, [t]) }
      cmds.push(RPG::EventCommand.new(355, 0, ['pfm_quest(:glyph_check, "Mum\'s Letter", "Find Imelda Larch at the research station on the headland.")']))
      CHECK_TRAINERS.each do |tt, name, double|
        script = (double ? 'setBattleRule("double"); ' : '') + "setBattleRule(\"canLose\"); TrainerBattle.start(:#{tt}, #{name.inspect})"
        cmds.push(RPG::EventCommand.new(355, 0, [script]))
      end
      cmds.push(RPG::EventCommand.new(0, 0, []))
      log("checks: #{CHECK_LINES.length} lines, quest log, #{CHECK_TRAINERS.length} trainer battles")
      pbMapInterpreter.setup(cmds, 0)
    end

    def drive_plan
      # After a blackout, do nothing until the rewind: otherwise wait_for_map would run the remaining steps as
      # "no way from map 101" while the Poke Center is still settling (seen 2026-11-19)
      if @rewind
        after_blackout if @idle >= 30
        return
      end
      if @reinstall
        debug_install if @idle >= 12 || @debug_phase
        return
      end
      step = plan[@step]
      return if !step
      kind, map = step
      if @step_start == 0
        @step_start = @frame
        @step_frames = 0
        log("step #{@step}: #{step.inspect}")
      end
      @step_frames += 1                # only frames with the map free count (cutscenes can be long)
      return wait_for_map if ![:done, :debug_install, :run_checks, :arrive, :need_map, :eval_conditions].include?(kind) &&
                             $game_map.map_id != map
      if @step_frames > 5400
        log("STUCK on step #{@step} #{step.inspect} at map #{$game_map.map_id} (#{$game_player.x},#{$game_player.y})")
        shot("stuck_step#{@step}")
        return next_step
      end
      case kind
      when :done
        return if @idle < 40
        @recording = false
        shot("end")
        log("plan done")
        finish
      when :debug_install
        return next_step if !["play", "narrative"].include?(SESSION) || $game_map.map_id != map
        debug_install if @idle >= 12
      when :run_checks
        run_checks if @idle >= 30
      when :need_map
        return next_step if map_installed?(map)
        return if @idle < 40
        @recording = false
        log("END OF RUN at step #{@step}: map #{map} is not installed (the rewiring has not landed); party #{party_text}")
        shot("end_map#{map}_missing")
        finish
      when :eval_conditions
        eval_conditions
        next_step
      when :arrive
        return wait_for_map if $game_map.map_id != map
        if @idle >= 60
          shot("arrived_map#{map}")
          next_step
        end
      else
        return wait_for_map if $game_map.map_id != map
        x, y = step[2], step[3]
        return ctrl_step($game_player.x, $game_player.y) if !$game_player.moving? && boxed_in?($game_player.x, $game_player.y)
        return (spot(step[2]) && next_step) if kind == :spot
        return spot_all if kind == :spot_all
        return catch_step if kind == :catch
        return to_map(step[2]) if kind == :to
        if x.is_a?(String)             # an event by name (it may wander)
          ev = $game_map.events.values.find { |e| e.name == x }
          return stuck("no event named #{x}") if !ev
          x, y = ev.x, ev.y
        end
        kind = :talk_near if kind == :near
        case kind
        when :goto
          return next_step if $game_player.x == x && $game_player.y == y && !$game_player.moving?
          walk_to(x, y)
        when :edge
          return walk_to(x, y) if $game_player.x != x || $game_player.y != y
          @dir = step[4] if !$game_player.moving?
        when :bump, :talk, :talk_near
          ax, ay, d = approach(x, y)
          if ax.nil? && kind == :talk && (path_dirs(x, y + 2) || [x, y + 2] == [$game_player.x, $game_player.y])
            ax, ay, d = x, y + 2, 8          # across a counter (Poke Center nurse)
          end
          return stuck("no tile next to (#{x},#{y})") if ax.nil?
          return walk_to(ax, ay) if $game_player.x != ax || $game_player.y != ay
          return next_step if kind == :talk_near
          return if @idle < 12
          if kind == :bump
            @dir = d
            @bumps = (@bumps || 0) + 1
            return stuck("bump did nothing") if @bumps > 300
          elsif $game_player.direction != d
            @dir = d
          elsif @talk_at && @went_busy && @went_busy > @talk_at
            next_step    # the event ran and is over
          elsif (@talk_n || 0) >= 4
            log("talk: nothing happened at #{step.inspect} (already done?)")
            next_step
          elsif !@talk_at || @frame - @talk_at > 120
            @talk_at = @frame
            @talk_n = (@talk_n || 0) + 1
            press(B::USE)
          end
        end
      end
    end

    # A step for another map: skip ahead to the first later step for the map we are on
    # The step is for another map. Skip ahead only over transit steps (arriving where a [:to] step leads, or an event
    # that carried the player on); otherwise walk back to the step's map over the plan's links (e.g. from a Poke Center
    # after a blackout) and never skip unfinished steps.
    def wait_for_map
      here = $game_map.map_id
      @map_wait = (@map_wait || 0) + 1
      later = plan[@step..].index { |s| s[1] == here }
      later = nil if later && plan[(@step + 1)...(@step + later)].any? { |s| s[0] != :to }
      if later
        @step += later
        @step_start = 0
        log("now on map #{here}: skipping to step #{@step}")
        return
      end
      target = plan[@step] && plan[@step][1]
      hop = target.is_a?(Integer) ? next_hop(here, target) : nil
      limit = hop ? 4000 : 1500          # per map: @map_wait restarts on every map change
      if @map_wait > limit
        log("GAVE UP on #{plan[@step].inspect}: still on map #{here} (#{$game_player.x},#{$game_player.y})")
        shot("gave_up_step#{@step}")
        return next_step
      end
      to_map(hop) if hop && @idle >= 12
    end

    # Next map on the shortest way from map `from` to map `dest`, over the links the plan's [:to, a, b] steps walk
    # (both ways), e.g. 101 -> 100 -> 520 -> 527 after a blackout on the Strand Road
    def next_hop(from, dest)
      @graph ||= begin
        g = Hash.new { |h, k| h[k] = [] }
        plan.each { |st| (g[st[1]] << st[2]; g[st[2]] << st[1]) if st[0] == :to }
        g.each_value(&:uniq!)
        g
      end
      return nil if from == dest
      prev = { from => nil }
      queue = [from]
      until queue.empty?
        m = queue.shift
        break if m == dest
        @graph[m].each { |n| next if prev.has_key?(n); prev[n] = m; queue.push(n) }
      end
      return nil if !prev.has_key?(dest)
      m = dest
      m = prev[m] while prev[m] != from
      return m
    end

    def next_step
      @step += 1
      @step_start = 0
      @bumps = 0
      @talk_at = nil
      @talk_n = 0
      @spot_i = 0; @spot_wait = 0; @map_wait = 0
      @path = nil
      autosave
      @nopath = 0
    end

    def stuck(why)
      log("STUCK step #{@step}: #{why} at (#{$game_player.x},#{$game_player.y}) map #{$game_map.map_id}")
      shot("stuck_step#{@step}")
      next_step
    end

    DIRS = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }

    # Tile to stand on to face (x, y): from below first (doors), then the sides, then above
    def approach(x, y)
      [[x, y + 1, 8], [x - 1, y, 6], [x + 1, y, 4], [x, y - 1, 2]].each do |ax, ay, d|
        next if !$game_map.valid?(ax, ay)
        return ax, ay, d if (ax == $game_player.x && ay == $game_player.y) || path_dirs(ax, ay)
      end
      return nil
    end

    # Tiles of touch events that transfer the player (door mats): a walking player steps around them
    def transfer_tiles
      ret = {}
      $game_map.events.each_value do |e|
        next if ![1, 2].include?(e.trigger) || !e.list
        ret[[e.x, e.y]] = true if e.list.any? { |c| c.code == 201 }
      end
      return ret
    end

    # BFS on the current map with the player's own passability
    def path_dirs(tx, ty, sx = $game_player.x, sy = $game_player.y)
      return [] if sx == tx && sy == ty
      avoid = transfer_tiles
      w = $game_map.width
      prev = { (sy * w) + sx => nil }
      queue = [[sx, sy]]
      until queue.empty?
        cx, cy = queue.shift
        DIRS.each do |d, (dx, dy)|
          nx, ny = cx + dx, cy + dy
          next if !$game_map.valid?(nx, ny)
          k = (ny * w) + nx
          next if prev.has_key?(k)
          next if avoid[[nx, ny]] && [nx, ny] != [tx, ty]
          next if !$game_player.passable?(cx, cy, d)
          prev[k] = [(cy * w) + cx, d]
          if nx == tx && ny == ty
            dirs = []
            while prev[k]
              dirs.unshift(prev[k][1])
              k = prev[k][0]
            end
            return dirs
          end
          queue.push([nx, ny])
        end
      end
      return nil
    end

    # Hold the arrow key for the next tile of a cached BFS path (recomputed when blocked or pushed off it)
    def walk_to(x, y)
      px, py = $game_player.x, $game_player.y
      if @path && @path_goal == [$game_map.map_id, x, y] && !@path.empty?
        if [px, py] != @path_at
          dx, dy = DIRS[@path[0]]
          if [px, py] == [@path_at[0] + dx, @path_at[1] + dy]
            @path.shift
            @path_at = [px, py]
          else
            @path = nil
          end
        end
      else
        @path = nil
      end
      if @path.nil? || @path.empty? || !$game_player.passable?(px, py, @path[0])
        @path = path_dirs(x, y)
        @path_goal = [$game_map.map_id, x, y]
        @path_at = [px, py]
        if @path.nil?
          @nopath = (@nopath || 0) + 1
          return stuck("no path to (#{x},#{y})") if @nopath > 120   # NPCs may step aside
          return
        end
        @nopath = 0
      end
      @dir = @path[0] || 0
    end

    # Walk into a trainer's line of sight: stand 2 (then 1, 3) tiles in front of it and wait to be noticed
    def spot(id)
      ev = $game_map.events[id]
      return true if !ev || $game_self_switches[[$game_map.map_id, id, "A"]] || @spot_i > 2
      dx, dy = DIRS[ev.direction] || [0, 1]
      d = [2, 1, 3][@spot_i]
      tx, ty = ev.x + (dx * d), ev.y + (dy * d)
      here = [tx, ty] == [$game_player.x, $game_player.y]
      if !$game_map.valid?(tx, ty) || (!here && !path_dirs(tx, ty))
        @spot_i += 1
        return false
      end
      return (walk_to(tx, ty); false) if !here
      @spot_wait += 1
      if @spot_wait > 90
        log("spot: trainer #{id} on map #{$game_map.map_id} did not notice at distance #{d} (party #{party_text})")
        @spot_i += 1
        @spot_wait = 0
      end
      return false
    end

    def spot_all
      @spot_skip ||= {}
      mid = $game_map.map_id
      list = $game_map.events.values.select { |e| e.name =~ /^Trainer\(/ && !$game_self_switches[[mid, e.id, "A"]] && !@spot_skip[[mid, e.id]] }
      return next_step if list.empty?
      @spot_cur = nil if @spot_cur && !list.any? { |e| e.id == @spot_cur }
      @spot_cur ||= list.min_by { |e| (e.x - $game_player.x).abs + (e.y - $game_player.y).abs }.id
      if spot(@spot_cur)
        if !$game_self_switches[[mid, @spot_cur, "A"]]
          log("spot_all: could not engage trainer event #{@spot_cur} on map #{mid}")
          @spot_skip[[mid, @spot_cur]] = true
        end
        @spot_cur = nil; @spot_i = 0; @spot_wait = 0
      end
    end

    # Tall grass until a second Pokemon joins (or the balls run out, or it takes too long)
    def catch_step
      return next_step if !want_catch?
      @catch_frames = @catch_frames.to_i + 1
      if @catch_frames > 5400
        log("catch: no catch after 90 s of grass (party #{party_text}, balls #{$bag.quantity(:POKEBALL)})")
        return next_step
      end
      if !@grass || @grass_map != $game_map.map_id
        @grass_map = $game_map.map_id
        @grass = []
        $game_map.width.times do |gx|
          $game_map.height.times { |gy| @grass.push([gx, gy]) if $game_map.terrain_tag(gx, gy).land_wild_encounters }
        end
        px, py = $game_player.x, $game_player.y
        @grass = @grass.sort_by { |g| (g[0] - px).abs + (g[1] - py).abs }.first(40).select { |g| path_dirs(g[0], g[1]) }
        log("catch: #{@grass.length} grass tiles near (#{px},#{py})")
        return next_step if @grass.length < 2
      end
      @grass_i = (@grass_i.to_i + 1) % @grass.length if [$game_player.x, $game_player.y] == @grass[@grass_i.to_i]
      g = @grass[@grass_i.to_i]
      walk_to(g[0], g[1])
    end

    # Does an edge arrival tile on another map connect to open ground (at least 40 tiles)?
    def open_arrival?(map, sx, sy)
      @arrival_ok ||= {}
      key = [map.map_id, sx, sy]
      return @arrival_ok[key] if @arrival_ok.has_key?(key)
      seen = { [sx, sy] => true }
      queue = [[sx, sy]]
      until queue.empty? || seen.length >= 40
        cx, cy = queue.shift
        DIRS.each do |d, (dx, dy)|
          nx, ny = cx + dx, cy + dy
          next if seen[[nx, ny]] || !map.valid?(nx, ny)
          next if !map.passable?(cx, cy, d, $game_player) || !map.passable?(nx, ny, 10 - d, $game_player)
          seen[[nx, ny]] = true
          queue.push([nx, ny])
        end
      end
      return @arrival_ok[key] = (seen.length >= 40)
    end

    # The transfer event (nearest) or the map edge that leads to map dest
    def to_map(dest)
      if !@to || @to[0] != [@step, $game_map.map_id]
        @to = [[@step, $game_map.map_id], nil]
        px, py = $game_player.x, $game_player.y
        evs = $game_map.events.values.select { |e| e.list && e.list.any? { |c| c.code == 201 && c.parameters[0] == 0 && c.parameters[1] == dest } }
        evs = evs.sort_by { |e| (e.x - px).abs + (e.y - py).abs }
        evs.each do |e|
          if path_dirs(e.x, e.y) then @to[1] = [:walk, e.x, e.y]
          elsif (ap = approach(e.x, e.y)) then @to[1] = [:bump, *ap]
          end
          break if @to[1]
        end
        if !@to[1]
          best = nil
          w, h = $game_map.width, $game_map.height
          edge = (0...w).flat_map { |ex| [[ex, 0, 8], [ex, h - 1, 2]] } + (0...h).flat_map { |ey| [[0, ey, 4], [w - 1, ey, 6]] }
          edge.each do |ex, ey, d|
            dx, dy = DIRS[d]
            nm = $map_factory.getNewMap(ex + dx, ey + dy)
            next if !nm || nm[0].map_id != dest || !$game_player.passable?(ex, ey, d)
            next if !open_arrival?(nm[0], nm[1], nm[2])   # don't walk off into the neighbour's tree line
            dist = (ex - px).abs + (ey - py).abs
            next if best && best[0] <= dist
            best = [dist, ex, ey, d] if [ex, ey] == [px, py] || path_dirs(ex, ey)
          end
          @to[1] = [:edge, best[1], best[2], best[3]] if best
        end
        log("to map #{dest}: #{@to[1].inspect}")
      end
      t = @to[1]
      if !t
        @to = nil
        return stuck("no way from map #{$game_map.map_id} to map #{dest}")
      end
      at = [$game_player.x, $game_player.y] == [t[1], t[2]]
      return walk_to(t[1], t[2]) if !at
      return if t[0] == :walk || $game_player.moving?
      @dir = t[3]
      @bumps = (@bumps || 0) + 1
      if @bumps > 400
        @to = nil
        stuck("holding #{t[3]} toward map #{dest} did nothing")
      end
    end

    def party_text
      return $player.party.map { |p| "#{p.species} L#{p.level} #{p.hp}/#{p.totalhp}" }.join(", ")
    end

    def map_installed?(id)
      infos = (pbLoadMapInfos rescue nil) || {}
      return infos.has_key?(id) && pbRgssExists?(sprintf("Data/Map%03d.rxdata", id))
    end

    # Every condition NarrativeCheck walks, evaluated against the live save (the static check only parses them)
    def eval_conditions
      list = Prismfall::NarrativeCheck.all_conditions
      bad = []
      list.each do |label, cond|
        Prismfall::Conditions.value(cond)
      rescue Exception => e
        bad.push("#{label}: #{e.class}: #{e.message}")
      end
      log("conditions: #{list.length} evaluated against the live save, #{bad.length} raised")
      bad.first(25).each { |b| log("  CONDITION ERROR #{b}") }
      Prismfall::Narrative::WARDEN_CONSENT.first(2).each_with_index do |c, i|
        g = (Prismfall::GYMS[i] rescue {}) || {}
        log("  consent row #{i + 1} (GYMS #{g[:index]} #{g[:warden]}): #{c} -> #{(Prismfall::Conditions.evaluate(c) rescue $!.class).inspect}")
      end
      log("  tally CONSENT = #{(Prismfall::Narrative.tally(:CONSENT) rescue $!.class).inspect} of #{Prismfall::Narrative::WARDEN_CONSENT.size}")
    rescue Exception => e
      log("conditions: evaluation failed #{e.class}: #{e.message}")
    end

    # The field and EBDX room a battle actually got, next to the map's default field
    def log_room(scene, battle)
      room = (PrismfallEBDX.ebdx_room(scene) rescue nil)
      data = room ? (room.instance_variable_get(:@data) || {}) : {}
      mid = $game_map ? $game_map.map_id : nil
      mapf = (FieldEffects::MAP_FIELDS[mid] rescue nil)
      fld = (battle.respond_to?(:field_effect) ? (battle.field_effect rescue "?") : "-")
      log("  room: field #{fld} (map #{mid} default #{mapf.inspect}) | EBDX backdrop #{data['backdrop'].inspect}" \
          "#{data['img000'] ? ' + HD layer' : ''} | essentials backdrop #{battle.backdrop rescue '?'}")
    rescue StandardError => e
      log("  room: #{e.class}: #{e.message}")
    end

    # Resilience: save and note the step after each step, so PLAYBOT_SESSION=resume can carry on after a host restart
    def autosave
      return if !["play", "resume"].include?(SESSION) || !ENV["PLAYBOT_STATE"] || !on_map? || @step < 2
      return if pbMapInterpreterRunning? || $game_temp.in_battle
      File.write(ENV["PLAYBOT_STATE"], "#{@step} #{@nframe} #{@blackouts.to_i}") if Game.save
    rescue StandardError => e
      log("autosave failed: #{e.message}")
    end

    def resume_state
      st = (File.read(ENV["PLAYBOT_STATE"]).split.map(&:to_i) rescue nil)
      return if !st
      @step, @nframe, @blackouts = st
      @step_start = 0
      @spot_i = 0; @spot_wait = 0; @map_wait = 0; @talk_n = 0; @bumps = 0; @nopath = 0   # what next_step resets
      @reinstall = (ENV["PLAYBOT_REINSTALL"] == "1")
      log("RESUMED from the autosave at step #{@step} #{plan[@step].inspect}" +
          (@reinstall ? " after a kit update: Debug > Files > Install Prismfall maps first" : " (host restart; not one unbroken run)"))
    end

    def blackout
      @blackouts = @blackouts.to_i + 1
      log("BLACKOUT ##{@blackouts} at step #{@step} #{plan[@step].inspect} on map #{$game_map.map_id}; party #{party_text}")
      shot("blackout_#{@blackouts}")
      @rewind = true
    end

    def after_blackout
      @rewind = false
      if @blackouts > MAX_BLACKOUTS
        log("STOPPING: #{@blackouts} blackouts (difficulty wall for this one-or-two-Pokemon AI team)")
        return finish
      end
      @step_start = 0
      @spot_i = 0; @spot_wait = 0; @map_wait = 0; @talk_n = 0; @bumps = 0; @nopath = 0; @path = nil; @to = nil
      log("after blackout: on map #{$game_map.map_id}, walking back to step #{@step} #{plan[@step].inspect}")
    end

    def want_catch?
      return $player.party.length < 2 && $bag && $bag.has?(:POKEBALL)
    end

    def boxed_in?(px, py)
      return DIRS.keys.none? { |d| $game_player.passable?(px, py, d) }
    end

    # The player stands on an impassable tile (a map bug: an arrival or start tile under a prop). In Debug mode a
    # tester holds Ctrl to walk through it; do the same for one step, onto the neighbour with the most open floor.
    def ctrl_step(px, py)
      best = nil
      [4, 6, 8, 2].each do |d|
        dx, dy = DIRS[d]
        nx, ny = px + dx, py + dy
        next if !$game_map.valid?(nx, ny)
        next if $game_map.events.values.any? { |e| e.x == nx && e.y == ny && e.trigger == 1 }  # not onto a door mat
        n = reach_count(nx, ny)
        best = [n, d] if !best || n > best[0]
      end
      return stuck("boxed in at (#{px},#{py}) with no way on") if !best || best[0] <= 1
      if !@seen["boxed#{$game_map.map_id},#{px},#{py}"]
        shot_once("boxed#{$game_map.map_id},#{px},#{py}", "BOXED_IN_map#{$game_map.map_id}_#{px}_#{py}")
        log("BOXED IN on map #{$game_map.map_id} (#{px},#{py}): Ctrl-walk (Debug walk-through) one step #{best[1]}")
      end
      @planning = false
      press(B::CTRL)
      @dir = best[1]
    end

    def reach_count(sx, sy, cap = 150)
      seen = { [sx, sy] => true }
      queue = [[sx, sy]]
      until queue.empty? || seen.length >= cap
        cx, cy = queue.shift
        DIRS.each do |d, (dx, dy)|
          nx, ny = cx + dx, cy + dy
          next if seen[[nx, ny]] || !$game_map.valid?(nx, ny) || !$game_player.passable?(cx, cy, d)
          seen[[nx, ny]] = true
          queue.push([nx, ny])
        end
      end
      return seen.length
    end

    # Debug > Files options > Install Prismfall maps. As a plan step it advances the plan; on a resume after a kit
    # update (PLAYBOT_REINSTALL=1) it runs once, then quits (restart); the next plain resume carries on.
    def debug_install
      done = proc do
        @debug_phase = :closed
        if @reinstall   # the installer says "Restart the game now": quit, and a plain resume carries on
          @reinstall = false
          log("reinstall done; quitting so the next resume restarts at step #{@step} #{plan[@step].inspect}")
          finish
        else
          next_step
        end
      end
      case @debug_phase
      when nil
        @debug_phase = :opening
        @debug_t = @frame
        log("debug: opening the Debug menu (F9)")
        press(B::F9)
      when :opening
        if @frame - @debug_t > 600
          log("debug: the menu never opened")
          done.call
        end
      when :leaving
        if @frame - @cmd_seen > 40
          log("debug: menu closed")
          done.call
        end
      else
        done.call
      end
    end

    def installer_ran
      @debug_phase = :leaving if @debug_phase == :open
    end
  end
end

#===============================================================================
# Hooks
#===============================================================================
module Graphics
  class << self
    alias playbot_update update unless method_defined?(:playbot_update)
    def update
      playbot_update
      PlayBot.tick
    end
  end
end

module Input
  class << self
    alias playbot_input_update update unless method_defined?(:playbot_input_update)
    def update
      playbot_input_update
      PlayBot.input_updated
    end
    alias playbot_trigger? trigger? unless method_defined?(:playbot_trigger?)
    alias playbot_press? press? unless method_defined?(:playbot_press?)
    alias playbot_repeat? repeat? unless method_defined?(:playbot_repeat?)
    alias playbot_dir4 dir4 unless method_defined?(:playbot_dir4)
    def trigger?(b); return true if PlayBot.pressed?(b); return playbot_trigger?(b); end
    def press?(b);   return true if PlayBot.pressed?(b); return playbot_press?(b);   end
    def repeat?(b);  return true if PlayBot.pressed?(b); return playbot_repeat?(b);  end
    def dir4
      d = PlayBot.dir
      return (d > 0) ? d : playbot_dir4
    end
  end
end

class Window_CommandPokemon
  alias playbot_update update unless method_defined?(:playbot_update)
  def update
    PlayBot.saw_cmd(self) if self.visible && self.active
    playbot_update
  end
end

class Window_AdvancedTextPokemon
  alias playbot_update update unless method_defined?(:playbot_update)
  def update
    PlayBot.saw_msg(self) if self.visible
    playbot_update
  end
end

alias playbot_pbMessageDisplay pbMessageDisplay unless defined?(playbot_pbMessageDisplay)
def pbMessageDisplay(msgwindow, message, *args, &block)
  PlayBot.last_text = message
  PlayBot.log("msg: #{message.to_s.gsub(/\s+/, ' ')[0, 140]}")
  return playbot_pbMessageDisplay(msgwindow, message, *args, &block)
end

class PokemonEntryScene2
  alias playbot_pbStartScene pbStartScene unless method_defined?(:playbot_pbStartScene)
  def pbStartScene(*args)
    playbot_pbStartScene(*args)
    PlayBot.entry = self
  end

  alias playbot_pbEndScene pbEndScene unless method_defined?(:playbot_pbEndScene)
  def pbEndScene
    PlayBot.entry = nil
    playbot_pbEndScene
  end
end

module PrismfallMapInstaller
  class << self
    alias playbot_install install unless method_defined?(:playbot_install)
    def install(**kwargs)
      PlayBot.log("installer: #{kwargs.inspect}")
      ret = playbot_install(**kwargs)
      PlayBot.installer_ran
      return ret
    end
  end
end

module Game
  class << self
    alias playbot_start_new start_new unless method_defined?(:playbot_start_new)
    def start_new
      PlayBot.log("New Game (session #{PlayBot::SESSION}); plugins: #{PluginManager.plugins.inspect}")
      PlayBot.recording = ["play", "ch1"].include?(PlayBot::SESSION)
      if ["route1", "checks", "ch1", "narrative"].include?(PlayBot::SESSION)   # dev shortcut: begin on Route 1's south edge, as after K1
        PrismfallMaps.define_singleton_method(:apply_start_position) do
          $data_system.start_map_id, $data_system.start_x, $data_system.start_y = 520, 16, 67
          true
        end
      end
      playbot_start_new
      if ["route1", "checks", "ch1", "narrative"].include?(PlayBot::SESSION)
        if PlayBot::SESSION == "ch1"   # what the prologue run had set by the time it reached Route 1
          [101, 102, 161].each { |i| $game_switches[i] = true }
          $game_variables[101] = $game_variables[102] = 1
          $player.has_pokedex = true
          Prismfall.record_starter(:MUDKIP, gen: 3, slot: 2)
          PrismfallMaps.set_first_respawn
          pfm_set(:starter_picked); pfm_set(:juno_errand)
        end
        $player.name = PlayBot::NAME
        $player.has_running_shoes = true
        $player.party = [Pokemon.new(:MUDKIP, (PlayBot::SESSION == "ch1") ? 10 : 7)]
        $player.party.push(Pokemon.new(:STARLY, 7)) if PlayBot::SESSION == "checks"   # doubles need two
        $game_switches[103] = $game_switches[104] = true
        $game_map.need_refresh = true
      end
      $PokemonSystem.textspeed = 2 if $PokemonSystem   # Fast
      $PokemonSystem.runstyle = 1 if $PokemonSystem    # run without holding Back
      PlayBot.log("started on map #{$game_map.map_id} (#{$game_player.x},#{$game_player.y}); respawn #{$PokemonGlobal.pokecenterMapId.inspect},#{$PokemonGlobal.pokecenterX.inspect},#{$PokemonGlobal.pokecenterY.inspect}; map 100 HealingSpot #{(GameData::MapMetadata.try_get(100)&.teleport_destination).inspect}")
    end
  end
end

# Test copy only: an event whose tile graphic is beyond its tileset stops the engine ("out-of-range tile", maps 521 and
# 525 after the tileset-53 rebuild, reported in mapgen/REQUESTS.md item 10). Draw nothing there and log it once.
class Game_Character
  alias playbot_screen_z screen_z unless method_defined?(:playbot_screen_z)
  def screen_z(height = 0)
    if @tile_id.to_i > 0 && self.map && @tile_id >= self.map.priorities.xsize
      PlayBot.log("MAP BUG: map #{self.map.map_id} event #{(@id rescue '?')} tile graphic #{@tile_id} is beyond the tileset; blanked")
      @tile_id = 0
    end
    return playbot_screen_z(height)
  end
end

alias playbot_pbStartOver pbStartOver unless defined?(playbot_pbStartOver)
def pbStartOver(*args)
  PlayBot.blackout
  return playbot_pbStartOver(*args)
end

# With Poke Balls and a one-Pokemon party, the bot throws a ball each turn of a wild battle (a new player's first catch)
class Battle::AI
  alias playbot_pbDefaultChooseEnemyCommand pbDefaultChooseEnemyCommand unless method_defined?(:playbot_pbDefaultChooseEnemyCommand)
  def pbDefaultChooseEnemyCommand(idxBattler)
    if @battle.wildBattle? && !@battle.opposes?(idxBattler) && !@battle.disablePokeBalls && PlayBot.want_catch? &&
       @battle.pbRegisterItem(idxBattler, :POKEBALL, 1)
      PlayBot.log("  bot throws a Poke Ball")
      return
    end
    playbot_pbDefaultChooseEnemyCommand(idxBattler)
  end
end

module Game
  class << self
    alias playbot_load load unless method_defined?(:playbot_load)
    def load(save_data)
      playbot_load(save_data)
      if PlayBot::SESSION == "resume"
        PlayBot.recording = true
        PlayBot.resume_state
        $PokemonSystem.textspeed = 2
        $PokemonSystem.runstyle = 1
      end
    end
  end
end

# AI plays the player's side (the Dovetail prologue never needs a human in battle)
module BattleCreationHelperMethods
  class << self
    alias playbot_prepare_battle prepare_battle unless method_defined?(:playbot_prepare_battle)
    def prepare_battle(battle)
      playbot_prepare_battle(battle)
      battle.controlPlayer = true
      who = battle.opponent ? battle.opponent.map { |t| t.full_name }.join(" + ") : "wild #{battle.pbParty(1).map { |p| "#{p.species} L#{p.level}" }.join(', ')}"
      fld = (battle.respond_to?(:field_effect) ? (battle.field_effect rescue "?") : "-")
      PlayBot.battle_tag = "#{fld}_#{who}"
      PlayBot.log("BATTLE map #{$game_map.map_id} vs #{who} | field #{fld} | backdrop #{battle.backdrop} | party #{PlayBot.party_text} | foe #{battle.pbParty(1).map { |p| "#{p.species} L#{p.level}" }.join(', ')}")
      PlayBot.log("battle prepared: #{battle.opponent ? battle.opponent.map { |t| t.full_name }.inspect : 'wild'} field #{battle.respond_to?(:field_effect) ? (battle.field_effect rescue '?') : '-'}")
    end
  end
end

class Battle::Scene
  alias playbot_loadBackdrop loadBackdrop unless method_defined?(:playbot_loadBackdrop)
  def loadBackdrop
    playbot_loadBackdrop
    PlayBot.log_room(self, @battle)
  end
end

class Battle
  alias playbot_pbCommandPhase pbCommandPhase unless method_defined?(:playbot_pbCommandPhase)
  def pbCommandPhase
    if PlayBot::SESSION == "checks" && @turnCount >= 2
      PlayBot.log("  checks: ending the battle after 2 turns")
      @decision = 3
      return
    end
    playbot_pbCommandPhase
  end

  alias playbot_pbEndOfBattle pbEndOfBattle unless method_defined?(:playbot_pbEndOfBattle)
  def pbEndOfBattle
    ret = playbot_pbEndOfBattle
    outcome = { 1 => "won", 2 => "lost", 3 => "ran/ended", 4 => "caught", 5 => "draw" }[@decision] || @decision.to_s
    PlayBot.log("BATTLE END: #{outcome} | party #{PlayBot.party_text rescue '?'}")
    return ret
  end

  alias playbot_pbDisplay pbDisplay unless method_defined?(:playbot_pbDisplay)
  def pbDisplay(msg, &block)
    PlayBot.log("  battle: #{msg}")
    playbot_pbDisplay(msg, &block)
  end
end

# Errors: log them with a screenshot instead of a blocking message box, then quit
alias playbot_pbPrintException pbPrintException unless defined?(playbot_pbPrintException)
def pbPrintException(e)
  PlayBot.fatal("#{e.class}: #{e.message}\n  " + (e.backtrace || [])[0, 25].join("\n  "))
  PlayBot.finish
end

# This Linux engine build (Ruby 3.3) leaves the stock scripts' top-level methods private, so stock
# pbMessage's `Kernel.pbShowCommands` (every choice box) raises NoMethodError. Official Windows builds
# have it public (Essentials could not show a choice otherwise): restore that here.
Object.send(:public, :pbShowCommands)

# No audio device here (and this engine build rejects Essentials' float positions)
module Audio
  class << self
    %w[bgm_play bgm_stop bgm_fade bgs_play bgs_stop bgs_fade me_play me_stop me_fade se_play se_stop].each do |m|
      define_method(m) { |*_args| nil }
    end
    def bgm_pos; 0; end
    def bgs_pos; 0; end
  end
end

PlayBot.log("bot loaded (session #{PlayBot::SESSION})")
