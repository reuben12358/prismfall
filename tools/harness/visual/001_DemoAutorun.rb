#===============================================================================
# DEV-ONLY capture tool (lives only in the run copy). Skips the title screen,
# starts a new game, runs scripted field battles with the AI playing both sides
# and dumps frames through Graphics.screenshot. Never ship this plugin.
#===============================================================================
module DemoRun
  ROOT = "Captures"
  @rec = nil; @frame = 0; @shots = 0; @every = 3; @auto = false
  # DEMO_SLOW=1: readable pacing for viewers (slow text, holds after every message, 1 s pause
  # before each turn, frame-locked clock, 30 fps PNG capture with a per-frame state log).
  SLOW          = (ENV["DEMO_SLOW"] == "1")
  HOLD_NORMAL   = 2.5    # seconds a finished message stays up
  HOLD_FIELD    = 3.5    # field / boss messages
  TURN_PAUSE    = 1.0
  @every = 2 if SLOW
  @idle = 0; @idle_text = nil
  class << self
    attr_accessor :every, :auto, :plan, :turn_limit, :script, :started, :scene, :change_turn,
                  :after_change_turns, :virtual_clock
    def log(msg)
      File.open("#{ROOT}/demo.log", "a") { |f| f.puts(msg) }
    end

    def record(name)
      @rec = "#{ROOT}/#{name}"
      Dir.mkdir(ROOT) if !Dir.exist?(ROOT)
      Dir.mkdir(@rec) if !Dir.exist?(@rec)
      @shots = 0
    end

    def stop; @rec = nil; end
    def frame; @frame; end

    def tick
      @frame += 1
      update_idle
      return if !@rec || @frame % @every != 0
      if SLOW
        Graphics.screenshot(format("%s/f%05d.png", @rec, @shots))
        w = msg_window
        state = (!w) ? "none" : (w.busy? && !w.pausing?) ? "typing" : "shown"
        txt = (w) ? w.text.to_s.gsub(/[\t\n\r]/, " ") : ""
        File.open("#{@rec}/frames.tsv", "a") do |f|
          f.puts([@shots, @frame, state, (state == "none") ? "" : (field_message?(txt) ? "field" : "normal"), txt].join("\t"))
        end
      else
        Graphics.screenshot(format("%s/f%05d.bmp", @rec, @shots))
      end
      @shots += 1
    end

    #---------------------------------------------------------------------------
    # Slow mode helpers
    #---------------------------------------------------------------------------
    # The battle message window, if it is up with text in it.
    def msg_window
      sc = @scene
      return nil if !sc
      sprites = sc.instance_variable_get(:@sprites)
      w = sprites && sprites["messageWindow"]
      return nil if !w || w.disposed? || !w.visible || w.text.to_s.empty?
      return w
    end

    # Frames the current text has been fully shown (typing finished, or paused at a \1).
    def update_idle
      w = msg_window
      if w && (!w.busy? || w.pausing?)
        if w.text == @idle_text
          @idle += 1
        else
          @idle_text = w.text; @idle = 1
        end
      else
        @idle = 0; @idle_text = nil
      end
    end

    def hold_frames(text)
      return ((field_message?(text) ? HOLD_FIELD : HOLD_NORMAL) * 60).round
    end

    # Ready to "press" Use on a prompt (yes/no, command list) whose text has been read.
    def prompt_ready?
      return false if @idle == 0 || @idle < hold_frames(@idle_text)
      @idle = 0
      return true
    end

    # Messages written in field definitions or boss definitions get the longer hold.
    def field_message?(text)
      return false if text.nil? || text.empty?
      @field_res ||= build_field_res
      plain = text.gsub(/\\[a-z]+\[[^\]]*\]/i, "").gsub("\1", "")
      return @field_res.any? { |re| plain =~ re }
    end

    def build_field_res
      strings = []
      skip = [:name, :backdrop, :description, :notes, :id]
      walk = lambda do |obj, key|
        case obj
        when Hash then obj.each { |k, v| walk.call(v, k) if !skip.include?(k) }
        when Array then obj.each { |v| walk.call(v, key) }
        when String then strings << obj if obj.length > 8
        end
      end
      FieldEffects.ids.each { |id| walk.call(FieldEffects.get(id), nil) } if defined?(FieldEffects)
      if defined?(Prismfall::Bosses)
        Prismfall::Bosses.ids.each { |id| walk.call(Prismfall::Bosses.get(id), nil) }
        walk.call(Prismfall::Bosses::BREAK_MESSAGE, nil) if Prismfall::Bosses.const_defined?(:BREAK_MESSAGE)
      end
      strings.uniq.map do |str|
        Regexp.new("\\A" + Regexp.escape(str).gsub(/\\\{\d\\\}/, ".+") + "\\z", Regexp::IGNORECASE)
      end
    end

    # Game time advances exactly 1/60 s per frame, so captured frames are real time even when
    # software rendering runs slower than 60 fps.
    def enable_virtual_clock
      return if @vbase
      @vbase = System.uptime
      @vframe = @frame
      self.virtual_clock = true
    end

    def virtual_uptime
      return @vbase + (@frame - @vframe) / 60.0
    end

    def mon(species, level, moves = nil, item = nil)
      p = Pokemon.new(species, level)
      GameData::Stat.each_main { |s| p.iv[s.id] = 31 }
      if moves
        p.forget_all_moves
        moves.each { |m| p.learn_move(m) }
      end
      p.item = item
      p.calc_stats
      p
    end

    def battle(name, party, turns: 99, script: nil)
      log("battle #{name} start")
      $player.party = party
      self.turn_limit = turns
      self.script = script
      self.change_turn = nil
      self.scene = nil
      record(name)
      self.auto = true
      begin
        yield
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(25).join("\n  "))
      end
      self.auto = false
      self.scene = nil
      40.times { Graphics.update }
      stop
      $game_temp.clear_battle_rules
      log("battle #{name} end (outcome var #{$game_variables[1]})")
    end

    def run
      self.started = true
      File.write("#{ROOT}/demo.log", "") rescue Dir.mkdir(ROOT)
      log("boot ok: plugins #{PluginManager.plugins.inspect}")
      Graphics.transition(0)            # Main leaves the screen frozen for the title scene
      # Battle captures must not depend on the overworld map pipeline: start on the base project's
      # own start map instead of Prismfall Maps' PRISMFALL_START (those maps need the custom tilesets
      # installed by mapgen/merge_tilesets.py). Done here because Prismfall Maps loads after this plugin.
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      $scene.createSpritesets           # what Scene_Map#main would do; EBDX intros snapshot the map
      30.times { Graphics.update; $scene.miniupdate }
      $player.name = "Tester"
      $PokemonSystem.textspeed = (SLOW) ? 0 : 2   # 0 = Slow (the slowest setting)
      enable_virtual_clock if SLOW
      self.after_change_turns = (SLOW) ? 1 : nil   # slow mode: end one turn after the field transition
      $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:CHARMANDER)
      $player.badges = Array.new(18) { true }
      Prismfall::LevelCap.unlock_finale!
      plan = (ENV["DEMO_PLAN"] || "volcanic").split(",")
      if plan.include?("volcanic")
        # Gym 7 (Brann) on the Volcanic Field; the lead only knows Surf, so two Surfs quench it.
        party = [mon(:VAPOREON, 39, [:SURF]), mon(:GRAVELER, 39, [:ROCKSLIDE, :BULLDOZE]),
                 mon(:AMPHAROS, 39, [:DISCHARGE, :POWERGEM])]
        battle("volcanic", party, :turns => (ENV["DEMO_TURNS"] || 5).to_i) do
          $player.badges = Array.new(18) { |i| i < 6 }
          Prismfall.gym_battle(7, :can_lose => true)
        end
      end
      if plan.include?("silkwood")
        party = [mon(:GROWLITHE, 15, [:EMBER], :TELLURICSEED), mon(:STARAVIA, 15), mon(:MAREEP, 15)]
        battle("silkwood", party, :turns => 6) do
          $player.badges = Array.new(18) { false }
          Prismfall.gym_battle(1, :can_lose => true)
        end
      end
      if plan.include?("zekrom")
        party = [mon(:GARCHOMP, 100, [:DRAGONCLAW, :EARTHQUAKE]), mon(:TOGEKISS, 100), mon(:LUCARIO, 100)]
        battle("zekrom", party, :turns => 4) do
          $player.badges = Array.new(18) { true }
          Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE, :can_lose => true)
        end
      end
      log("done")
    end
  end
end

module Graphics
  class << self
    alias demo_autorun_update update unless method_defined?(:demo_autorun_update)
    def update
      demo_autorun_update
      DemoRun.tick
    end
  end
end

# Auto-advance message boxes: "press" Use every 24th frame while a demo battle runs, and
# during boot (first boot of a fresh copy shows Essentials' "N new map(s) ... imported" box).
module Input
  class << self
    alias demo_autorun_trigger? trigger? unless method_defined?(:demo_autorun_trigger?)
    def trigger?(button)
      if button == Input::USE
        if DemoRun::SLOW && DemoRun.auto
          if DemoRun.msg_window
            return true if DemoRun.prompt_ready?
          elsif DemoRun.frame % (DemoRun::HOLD_NORMAL * 60).round == 0
            return true                     # any other dialog: one press per 2.5 s
          end
        elsif (DemoRun.auto || !DemoRun.started) && DemoRun.frame % 24 == 0
          return true
        end
      end
      return demo_autorun_trigger?(button)
    end
  end
end

# AI plays the player's side; stop after the planned number of turns.
module BattleCreationHelperMethods
  class << self
    alias demo_autorun_prepare_battle prepare_battle unless method_defined?(:demo_autorun_prepare_battle)
    def prepare_battle(battle)
      demo_autorun_prepare_battle(battle)
      if DemoRun.auto
        battle.controlPlayer = true
        DemoRun.scene = battle.scene
      end
    end
  end
end

class Battle
  alias demo_autorun_pbCommandPhase pbCommandPhase unless method_defined?(:demo_autorun_pbCommandPhase)
  def pbCommandPhase
    if DemoRun.auto && DemoRun.turn_limit && @turnCount >= DemoRun.turn_limit
      DemoRun.log("turn limit reached at turn #{@turnCount}")
      @decision = 3
      return
    end
    if DemoRun.auto && DemoRun.change_turn && DemoRun.after_change_turns &&
       @turnCount >= DemoRun.change_turn + 1 + DemoRun.after_change_turns   # change_turn = 0-based turn index
      DemoRun.log("stopping #{DemoRun.after_change_turns} turn(s) after the field change")
      @decision = 3
      return
    end
    if DemoRun::SLOW && DemoRun.auto
      (DemoRun::TURN_PAUSE * 60).round.times { @scene.pbUpdate }
    end
    DemoRun.log("turn #{@turnCount + 1}: field #{field_effect} " +
                allBattlers.map { |b| "#{b.name} #{b.hp}/#{b.totalhp}" }.join(" | "))
    demo_autorun_pbCommandPhase
  end

  alias demo_autorun_pbDisplay pbDisplay unless method_defined?(:demo_autorun_pbDisplay)
  def pbDisplay(msg, &block)
    DemoRun.log("  msg: #{msg}")
    demo_autorun_pbDisplay(msg, &block)
  end
end

class Scene_DemoRun
  def main
    begin
      DemoRun.run
    rescue Exception => e
      raise if e.is_a?(SystemExit)
      detail = (e.respond_to?(:event_message) && e.event_message) ? "\n" + e.event_message.to_s : ""
      DemoRun.log("FATAL #{e.class}: #{e.message}#{detail}\n  " + (e.backtrace || []).first(30).join("\n  "))
    end
    $scene = nil
    Kernel.exit!(0)
  end
end

alias demo_autorun_pbCallTitle pbCallTitle unless defined?(demo_autorun_pbCallTitle)
def pbCallTitle
  return Scene_DemoRun.new
end

# No audio device in the capture environment (and this engine build's audio binding rejects
# Essentials' float positions): silence every Audio call.
module Audio
  class << self
    %w[bgm_play bgm_stop bgm_fade bgs_play bgs_stop bgs_fade me_play me_stop me_fade se_play se_stop].each do |m|
      define_method(m) { |*_args| nil }
    end
    def bgm_pos; 0; end
    def bgs_pos; 0; end
  end
end

#===============================================================================
# Slow mode: message holds (replaces EBDX's 1-second auto-close and brief messages)
#===============================================================================
class Battle::Scene
  alias demo_slow_pbDisplayMessage pbDisplayMessage unless method_defined?(:demo_slow_pbDisplayMessage)
  def pbDisplayMessage(msg, brief = false, &block)
    return demo_slow_pbDisplayMessage(msg, brief, &block) if !(DemoRun::SLOW && DemoRun.auto)
    pbWaitMessage
    pbShowWindow(MESSAGE_BOX)
    cw = @sprites["messageWindow"]
    cw.setText(msg)
    PBDebug.log_message(msg)
    demo_slow_hold(cw, msg, &block)
    if brief
      @briefMessage = true          # stays up while the next thing happens, as in normal play
    else
      cw.text = ""
      cw.visible = false
    end
  end

  alias demo_slow_pbDisplayPausedMessage pbDisplayPausedMessage unless method_defined?(:demo_slow_pbDisplayPausedMessage)
  def pbDisplayPausedMessage(msg, &block)
    return demo_slow_pbDisplayPausedMessage(msg, &block) if !(DemoRun::SLOW && DemoRun.auto)
    pbWaitMessage
    pbShowWindow(MESSAGE_BOX)
    cw = @sprites["messageWindow"]
    cw.text = msg
    PBDebug.log_message(msg)
    demo_slow_hold(cw, msg, &block)
    cw.text = ""
    cw.visible = false
  end

  def demo_slow_hold(cw, msg)
    hold = DemoRun.hold_frames(msg)
    yielded = false
    shown = 0
    loop do
      pbUpdate(cw)
      if !cw.busy? || cw.pausing?
        if !yielded
          yield if block_given?
          yielded = true
        end
        shown += 1
        if shown >= hold
          break if !cw.busy?
          cw.resume              # a \1 pause inside the text: continue typing
          shown = 0
        end
      end
    end
  end
end

module System
  class << self
    alias demo_slow_uptime uptime unless method_defined?(:demo_slow_uptime)
    def uptime
      return DemoRun.virtual_uptime if DemoRun.virtual_clock
      return demo_slow_uptime
    end
  end
end

EventHandlers.add(:prismfall_field_changed, :demo_autorun_change_turn,
  proc { |battle, old_id, new_id|
    next if !DemoRun.auto || old_id == :NONE || DemoRun.change_turn
    DemoRun.change_turn = battle.turnCount
    DemoRun.log("field change #{old_id} -> #{new_id} at turn #{battle.turnCount}")
  }
)
