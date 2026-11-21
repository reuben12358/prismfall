#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Glass Dunes stage captures (SPINE Rev 24): real battles where both
# sides' moves are scripted turn by turn, every Nth engine frame dumped to Captures/<plan>/.
#   DEMO_PLAN=glassstages             both plans below
#   GS_PLANS=cool,shatter             cool:    Hot Glass, 4 rounds without Fire -> Mirror Glass, then Double Team
#                                     shatter: Mirror Glass, three Boombursts crack it apart -> Desert
#   GS_EVERY=3                        dump every Nth frame (default 3)
#   GS_PRESS=70                       frames between auto-presses of a message (readable at half speed)
# Daytime forced. Loads after 001_DemoAutorun.rb (same "ZZ Demo Autorun" folder).
#===============================================================================
module GlassStageCapture
  PLANS = {
    "cool"    => { :stage => 1, :mon => [:WHISMUR, 60], :foe => [:BRONZONG, 70],
                   :mine   => [:HOWL, :CALMMIND, :CALMMIND, :CALMMIND, :DOUBLETEAM, :SPLASH],
                   :theirs => [:IRONDEFENSE, :CALMMIND, :CALMMIND, :IRONDEFENSE, :SPLASH, :SPLASH] },
    "shatter" => { :stage => 2, :mon => [:WHISMUR, 60], :foe => [:SNORLAX, 70],
                   :mine   => [:BOOMBURST, :BOOMBURST, :BOOMBURST, :SPLASH],
                   :theirs => [:IRONDEFENSE, :IRONDEFENSE, :IRONDEFENSE, :SPLASH] }
  }
  class << self
    attr_accessor :plan
  end
  module_function

  def run_all
    (ENV["GS_PLANS"] || "cool,shatter").split(",").each do |name|
      pl = PLANS[name] or next
      self.plan = pl
      DemoRun.every = (ENV["GS_EVERY"] || 3).to_i
      DemoRun.battle("gs_#{name}", [DemoRun.mon(pl[:mon][0], pl[:mon][1], [pl[:mine][0]])], :turns => 99) do
        $game_temp.clear_battle_rules
        setBattleRule("field", :GLASS_DUNES)
        setBattleRule("fieldStage", pl[:stage]) if pl[:stage] > 1
        WildBattle.start(pl[:foe][0], pl[:foe][1])
      end
      DemoRun.every = 100000
      self.plan = nil
    end
  end

  def set_move(battle, battler, move)
    battler.moves.clear
    battler.moves.push(Battle::Move.from_pokemon_move(battle, Pokemon::Move.new(move)))
  end
end

if ENV["DEMO_PLAN"].to_s.start_with?("glassstages")
  class << DemoRun
    alias gs_orig_run run unless method_defined?(:gs_orig_run)
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("glass stage capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      $scene.createSpritesets
      30.times { Graphics.update; $scene.miniupdate }
      $player.name = "Tester"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:CHARMANDER) rescue nil
      $player.badges = Array.new(18) { true }
      Prismfall::LevelCap.unlock_finale! rescue nil
      self.every = 100000
      GlassStageCapture.run_all
      log("done")
    end
  end

  module PBDayNight
    class << self
      def isNight?(*a);   false; end
      def isEvening?(*a); false; end
      def isMorning?(*a); false; end
      def isDay?(*a);     true;  end
    end
  end

  # One press every GS_PRESS frames while a battle runs, so each message stays up long enough to read.
  module Input
    class << self
      alias gs_trigger? trigger? unless method_defined?(:gs_trigger?)
      def trigger?(button)
        if button == Input::USE && DemoRun.auto
          return DemoRun.frame % (ENV["GS_PRESS"] || 70).to_i == 0
        end
        return gs_trigger?(button)
      end
    end
  end

  class Battle
    alias gs_pbCommandPhase pbCommandPhase unless method_defined?(:gs_pbCommandPhase)
    def pbCommandPhase
      pl = GlassStageCapture.plan
      if DemoRun.auto && pl
        t = @turnCount
        if t >= pl[:mine].length
          40.times { @scene.pbUpdate }
          @decision = 3
          return
        end
        allBattlers.each do |b|
          GlassStageCapture.set_move(self, b, (b.opposes? ? pl[:theirs] : pl[:mine])[t])
        end
        DemoRun.log("turn #{t + 1}: field #{field_effect} stage #{field_stage}")
      end
      gs_pbCommandPhase
    end
  end
end
