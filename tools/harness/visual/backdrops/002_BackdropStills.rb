#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Backdrop stills: one wild battle
# per field, held on the first command phase so the room's animated layers and
# the Bridge's particles run for a while, then Graphics.screenshot.
#   DEMO_PLAN=backdrops            all registered fields (+ every stage)
#   BD_FIELDS=VOLCANIC,FLOWER_GARDEN:3   only these
#   BD_TIME=day|night|eve          forces PBDayNight (default day)
#   BD_WAIT=150                    frames to run before the shot
#   BD_VECTORS=1                   also shoot the PLAYER / ENEMY / SENDOUT camera framings
# Output: Captures/backdrops/<field>[_s<stage>][_<time>].png (+ _clean = no databoxes)
#===============================================================================
module BackdropStills
  FOES = {
    :SILKWOOD => :GALVANTULA, :GRAND_STAGE => :MELOETTA, :WATER_SURFACE => :LAPRAS, :NEON_GRID => :ROTOM,
    :DESERT => :FLYGON, :CORROSIVE_MIRE => :MUK, :VOLCANIC => :TORKOAL, :COLOSSEUM => :MACHAMP,
    :FLOWER_GARDEN => :FLORGES, :FROZEN_LAKE => :WALREIN, :STORMFRONT => :TORNADUS, :MINDSCAPE => :GARDEVOIR,
    :CRYSTAL_CAVERN => :CARBINK, :HOLLOW_CATHEDRAL => :CHANDELURE, :FACTORY => :KLINKLANG, :NEW_MOON => :DARKRAI,
    :FAIRY_TALE => :SYLVEON, :DRAGONS_DEN => :HAXORUS, :CAVE => :GOLBAT, :MOUNTAIN => :SKARMORY,
    :SNOWY_MOUNTAIN => :ABOMASNOW, :BEACH => :KINGLER, :UNDERWATER => :LANTURN, :RAINBOW => :HOOH,
    :WASTELAND => :GARBODOR, :ASHEN_WASTE => :COALOSSAL, :DARK_CRYSTAL => :SABLEYE, :SCRAPYARD => :MAGNEZONE,
    :INVERSE => :GIRATINA, :BLEED => :PORYGONZ, :PRISM_ARENA => :ARCEUS
  }
  module_function

  def time_mode; (ENV["BD_TIME"] || "day").downcase; end

  def targets
    list = []
    if ENV["BD_FIELDS"] && !ENV["BD_FIELDS"].empty?
      ENV["BD_FIELDS"].split(",").each do |t|
        id, st = t.split(":")
        list << [id.to_sym, (st || 1).to_i]
      end
    else
      FieldEffects.ids.sort_by(&:to_s).each do |id|
        n = (FieldEffects.respond_to?(:max_stage) ? FieldEffects.max_stage(id) : 1) || 1
        (1..n).each { |s| list << [id, s] }
      end
    end
    list
  end

  def shot_name(id, stage)
    n = id.to_s.downcase
    n += "_s#{stage}" if stage > 1
    n += "_#{time_mode}" if time_mode != "day"
    n
  end

  def run_all
    Dir.mkdir("Captures/backdrops") if !Dir.exist?("Captures/backdrops")
    targets.each do |id, stage|
      next if !FieldEffects.exists?(id)
      @current = [id, stage]
      @done = false
      foe = FOES[id] || :DITTO
      foe = :DITTO if !GameData::Species.exists?(foe)
      party = [DemoRun.mon(:LUCARIO, 50, [:AURASPHERE])]
      DemoRun.battle("bd_#{shot_name(id, stage)}", party, :turns => 1) do
        $game_temp.clear_battle_rules
        setBattleRule("field", id)
        setBattleRule("fieldStage", stage) if stage > 1
        WildBattle.start(foe, 50)
      end
      DemoRun.log("backdrop still #{id} stage #{stage}: #{@done ? 'ok' : 'NO SHOT'}")
    end
  end

  def hold_and_shoot(scene)
    return if @done || !@current
    @done = true
    wait = (ENV["BD_WAIT"] || 150).to_i
    wait.times { scene.pbUpdate }
    name = shot_name(*@current)
    Graphics.screenshot("Captures/backdrops/#{name}.png")
    sprites = scene.sprites
    hidden = []
    sprites.each { |k, s| next if !k.to_s.start_with?("dataBox"); next if !s || s.disposed? || !s.visible; s.visible = false; hidden << s }
    3.times { scene.pbUpdate }
    Graphics.screenshot("Captures/backdrops/#{name}_clean.png")
    hidden.each { |s| s.visible = true }
    return if ENV["BD_VECTORS"] != "1"
    # other camera framings EBDX uses during a battle (move animations, send-out)
    [[:PLAYER, "player"], [:ENEMY, "enemy"], [:SENDOUT, "wide"]].each do |vec, tag|
      v = EliteBattle.get_vector(vec, scene.battle) rescue nil
      next if !v
      scene.vector.set(v)
      60.times { scene.pbUpdate }
      Graphics.screenshot("Captures/backdrops/#{name}_#{tag}.png")
    end
    scene.vector.reset
    20.times { scene.pbUpdate }
  end
end

if ENV["DEMO_PLAN"].to_s.start_with?("backdrops")
  class << DemoRun
    alias bd_orig_run run unless method_defined?(:bd_orig_run)
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("backdrop stills boot ok")
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
      self.every = 100000   # no frame dumps, stills only
      BackdropStills.run_all
      log("done")
    end
  end

  module PBDayNight
    class << self
      alias bd_isNight isNight? unless method_defined?(:bd_isNight)
      alias bd_isDay isDay? unless method_defined?(:bd_isDay)
      alias bd_isEvening isEvening? unless method_defined?(:bd_isEvening)
      alias bd_isMorning isMorning? unless method_defined?(:bd_isMorning)
      def isNight?(*a);   BackdropStills.time_mode == "night"; end
      def isEvening?(*a); BackdropStills.time_mode == "eve"; end
      def isMorning?(*a); false; end
      def isDay?(*a);     BackdropStills.time_mode == "day"; end
    end
  end

  class Battle
    alias bd_pbCommandPhase pbCommandPhase unless method_defined?(:bd_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        BackdropStills.hold_and_shoot(@scene)
        @decision = 3
        return
      end
      bd_pbCommandPhase
    end
  end
end
