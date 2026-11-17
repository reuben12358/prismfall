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
  PLAN = [
    [:debug_install, 109],
    [:goto, 109, 15, 10],          # cabin hatch -> 110
    [:talk, 110, 4, 7],            # Mum's letter
    [:goto, 110, 7, 11],           # back up to the deck
    [:goto, 109, 12, 6],           # rail: Edda
    [:goto, 109, 12, 7],
    [:goto, 109, 11, 6],           # rail again: Voss, docking
    [:goto, 109, 9, 15],           # gangway -> Ferrow's Landing
    [:goto, 100, 34, 47],          # Edda's last call (34,51), customs gate NULL scan
    [:bump, 100, 47, 10],          # Larch Research Station door -> 103
    [:talk, 103, 20, 10],          # starter table
    [:goto, 103, 14, 15],          # exit -> K1 autorun at the lab gate
    [:edge, 100, 34, 0, 8],        # north lane -> Route 1
    [:goto, 520, 12, 54],          # Juno's catching tutorial
    [:goto, 520, 16, 45],          # up the route (Route 1 trainers may spot us)
    [:done]
  ]

  @frame = 0; @press = {}; @dir = 0; @step = 0; @step_start = 0; @idle = 0
  @cmd = nil; @cmd_seen = -10; @cmd_key = nil; @cmd_target = nil; @cmd_since = 0; @cmd_moved = 0
  @cmd_used = {}; @msgwin = nil; @msg_seen = -10; @msg_pause = 0; @msg_wait = 0; @last_text = ""
  @seen = {}; @nshot = 0; @nframe = 0; @recording = false; @fatal = nil; @use_tick = 0
  @map_arrival = nil; @battle_frames = 0; @debug_phase = nil; @entry = nil; @step_ran_event = false
  @last_map = nil; @ready = 0; @went_busy = 0; @typed = 0; @entry_done = false

  class << self
    attr_accessor :recording, :debug_phase
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

    def press(button);  @press[button] = @frame; end
    def pressed?(b);    return @press[b] == @frame; end
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

    def map_idle?
      return map_ready? && !$game_player.moving? && !$game_player.jumping?
    end

    def brain
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
      end
      @went_busy = @frame
      @ready = 0
      @idle = 0
    end

    def track_map
      return if !on_map?
      id = $game_map.map_id
      if id != @last_map
        log("on map #{id} #{$game_map.name rescue '?'} at (#{$game_player.x},#{$game_player.y})")
        @last_map = id
        @map_arrival = @frame
        @path = nil
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
        @debug_phase = :open if find.call(/^Files options/) || find.call(/^Install Prismfall maps/)
        if @debug_phase == :open
          return find.call(/^Files options/) if find.call(/^Files options/) && !@cmd_used[:files]
          return find.call(/^Install Prismfall maps/) if find.call(/^Install Prismfall maps/) && !@cmd_used[:install]
          return :back
        end
      end
      return :back if @debug_phase == :leaving
      rules = [/^New Game$/, /Style A/, /^Standard$/, /^That's right\.$/, /^Nerve\.$/, /^Thank you\.$/,
               /^I'm staying\.$/, /^Drink it\.$/, /^It said NULL\.$/, /^Generation 3$/, /^Water: /,
               /^I was born here\.$/, /^Why not\?$/, /^I'm fine\.$/, /^Who\?$/]
      rules.each { |re| i = find.call(re); return i if i }
      if c.length == 2 && c[0] =~ /^Yes$/i && c[1] =~ /^No$/i
        return 0 if t =~ /Play on|install them now|give up|stop trying|stop learning/i
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
        @cmd_used[:files] = true if label =~ /^Files options/ && @debug_phase == :open
        @cmd_used[:install] = true if label =~ /^Install Prismfall maps/ && @debug_phase == :open
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
        if pos.nil?
          log("entry: '#{NAME[@typed]}' not on page #{mode}")
          @typed += 1
          return
        end
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
      shot("battle_start") if @battle_frames == 150
      shot("battle_t#{@battle_frames}") if @battle_frames > 150 && @battle_frames % 900 == 0
      press(B::USE) if @battle_frames % 20 == 0
    end

    #---------------------------------------------------------------------------
    # Plan steps (run while the map is free; walking keeps going while moving)
    #---------------------------------------------------------------------------
    def drive_plan
      step = PLAN[@step]
      return if !step
      kind, map = step
      if @step_start == 0
        @step_start = @frame
        @step_busy0 = @went_busy
        log("step #{@step}: #{step.inspect}")
      end
      if @frame - @step_start > 5400
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
        return next_step if SESSION != "play" || $game_map.map_id != map
        debug_install if @idle >= 12
      else
        return wait_for_map if $game_map.map_id != map
        x, y = step[2], step[3]
        case kind
        when :goto
          return next_step if $game_player.x == x && $game_player.y == y && !$game_player.moving?
          walk_to(x, y)
        when :edge
          return walk_to(x, y) if $game_player.x != x || $game_player.y != y
          @dir = step[4] if !$game_player.moving?
        when :bump, :talk
          ax, ay, d = approach(x, y)
          return stuck("no tile next to (#{x},#{y})") if ax.nil?
          return walk_to(ax, ay) if $game_player.x != ax || $game_player.y != ay
          return if @idle < 12
          if kind == :bump
            @dir = d
            @bumps = (@bumps || 0) + 1
            return stuck("bump did nothing") if @bumps > 300
          elsif $game_player.direction != d
            @dir = d
          elsif @talk_at && @went_busy && @went_busy > @talk_at
            next_step    # the event ran and is over
          elsif !@talk_at || @frame - @talk_at > 120
            @talk_at = @frame
            press(B::USE)
          end
        end
      end
    end

    # A step for another map: skip ahead to the first later step for the map we are on
    def wait_for_map
      later = PLAN[@step..].index { |s| s[1] == $game_map.map_id }
      return if !later
      @step += later
      @step_start = 0
      log("now on map #{$game_map.map_id}: skipping to step #{@step}")
    end

    def next_step
      @step += 1
      @step_start = 0
      @bumps = 0
      @talk_at = nil
      @path = nil
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

    # BFS on the current map with the player's own passability
    def path_dirs(tx, ty)
      sx, sy = $game_player.x, $game_player.y
      return [] if sx == tx && sy == ty
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

    def debug_install
      case @debug_phase
      when nil
        @debug_phase = :opening
        @debug_t = @frame
        log("debug: opening the Debug menu (F9)")
        press(B::F9)
      when :opening
        if @frame - @debug_t > 600
          log("debug: the menu never opened")
          @debug_phase = :closed
          next_step
        end
      when :leaving
        if @frame - @cmd_seen > 40
          log("debug: menu closed")
          @debug_phase = :closed
          next_step
        end
      else
        next_step
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
      PlayBot.recording = (PlayBot::SESSION == "play")
      playbot_start_new
      $PokemonSystem.textspeed = 2 if $PokemonSystem   # Fast
      $PokemonSystem.runstyle = 1 if $PokemonSystem    # run without holding Back
      PlayBot.log("started on map #{$game_map.map_id} (#{$game_player.x},#{$game_player.y})")
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
      PlayBot.log("battle prepared: #{battle.opponent ? battle.opponent.map { |t| t.full_name }.inspect : 'wild'} field #{battle.respond_to?(:field_effect) ? (battle.field_effect rescue '?') : '-'}")
    end
  end
end

class Battle
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
