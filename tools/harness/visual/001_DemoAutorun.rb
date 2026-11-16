#===============================================================================
# DEV-ONLY capture tool (lives only in the run copy). Skips the title screen,
# starts a new game, runs scripted field battles with the AI playing both sides
# and dumps frames through Graphics.screenshot. Never ship this plugin.
#===============================================================================
module DemoRun
  ROOT = "Captures"
  @rec = nil; @frame = 0; @shots = 0; @every = 3; @auto = false
  class << self
    attr_accessor :every, :auto, :plan, :turn_limit, :script
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
      return if !@rec || @frame % @every != 0
      Graphics.screenshot(format("%s/f%05d.bmp", @rec, @shots))
      @shots += 1
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
      record(name)
      self.auto = true
      begin
        yield
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(25).join("\n  "))
      end
      self.auto = false
      40.times { Graphics.update }
      stop
      $game_temp.clear_battle_rules
      log("battle #{name} end (outcome var #{$game_variables[1]})")
    end

    def run
      File.write("#{ROOT}/demo.log", "") rescue Dir.mkdir(ROOT)
      log("boot ok: plugins #{PluginManager.plugins.inspect}")
      Game.start_new
      $player.name = "Reuben" if false
      $player.name = "Tester"
      $PokemonSystem.textspeed = 2 rescue nil
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
        party = [mon(:GROWLITHE, 15, [:EMBER, :BITE], :TELLURICSEED), mon(:STARAVIA, 15), mon(:MAREEP, 15)]
        battle("silkwood", party, :turns => 5) do
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

# Auto-advance message boxes: "press" Use every 24th frame while a demo battle runs.
module Input
  class << self
    alias demo_autorun_trigger? trigger? unless method_defined?(:demo_autorun_trigger?)
    def trigger?(button)
      return true if DemoRun.auto && button == Input::USE && DemoRun.frame % 24 == 0
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
      battle.controlPlayer = true if DemoRun.auto
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
      DemoRun.log("FATAL #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(30).join("\n  "))
    end
    $scene = nil
    Kernel.exit!(0)
  end
end

alias demo_autorun_pbCallTitle pbCallTitle unless defined?(demo_autorun_pbCallTitle)
def pbCallTitle
  return Scene_DemoRun.new
end
