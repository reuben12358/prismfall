#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Battler placement probe: one wild
# battle per case, held on the first command phase, then for each camera framing
# a screenshot plus one probe row per battler (where EBDX anchors it, where the
# sprite's lowest opaque row lands on screen, and the room transform), so the
# painted bases can be compared with the real anchors.
#   DEMO_PLAN=placement
#   PP_CASES="MEADOW:TAUROS/LUCARIO;GRAND_STAGE:JOLTIK/SNORLAX;NEW_MOON:3:GASTLY/BIDOOF"
#                     field[:stage]:FOE/PLAYER (player defaults to LUCARIO)
#                     doubles: field[:stage]:FOE1+FOE2/PLAYER1+PLAYER2 (a double wild battle)
#   PP_VECTORS=1      also the ENEMY (intro close-up), SENDOUT (pull-back) and PLAYER framings
#   PP_INTRO=<case#>[,<case#>...]  dump every 2nd frame of those cases from the battle start (GIF source), with
#                     Captures/placement/intro_<case>.tsv: per dumped frame, the room camera and both battlers
#   PP_WAIT=150       frames to run before the MAIN shot
#   PP_GROUND=0       turn the Bridge's sprite grounding off (EBDX's own species metrics: "before" shots)
#   PP_FOOT=16,-2 PP_RAISE=0   an earlier FOOT_LINE / PLAYER_RAISE (with PP_GRAPHICS = that version's rooms)
#   PP_ROOM_RAISE=0   ignore the rooms' own extra player raise (profile :player_raise)
# Output: Captures/placement/<case>_<view>.png (+ _clean without databoxes), Captures/placement/probe.tsv
#===============================================================================
module PlacementProbe
  module_function

  def cases
    (ENV["PP_CASES"] || "MEADOW:TAUROS/LUCARIO").split(";").map do |c|
      parts = c.split(":")
      mons = parts.pop.split("/")
      id = parts[0].to_sym
      st = (parts[1] || 1).to_i
      [id, st, mons[0].split("+").map(&:to_sym), (mons[1] || "LUCARIO").split("+").map(&:to_sym)]
    end
  end

  def name_of(id, st, foe, pl)
    n = id.to_s.downcase
    n += "_s#{st}" if st > 1
    "#{n}__#{foe.map(&:to_s).join('+').downcase}__#{pl.map(&:to_s).join('+').downcase}"
  end

  def run_all
    Dir.mkdir("Captures/placement") if !Dir.exist?("Captures/placement")
    @tsv = "Captures/placement/probe.tsv"
    File.write(@tsv, %w[case view idx species anchor_x anchor_y spr_x spr_y ox oy zoom_x zoom_y bmp_w bmp_h
                        feet_row feet_l feet_r top_row bg_x bg_y bg_ox bg_oy bg_zx bg_zy shadow_vis].join("\t") + "\n")
    intro = (ENV["PP_INTRO"] || "-1").split(",").map(&:to_i)
    cases.each_with_index do |(id, st, foe, pl), ci|
      next if !FieldEffects.exists?(id)
      next if (foe + pl).any? { |sp| !GameData::Species.exists?(sp) }
      @current = name_of(id, st, foe, pl)
      @done = false
      DemoRun.every = intro.include?(ci) ? 2 : 100000
      @intro_tsv = nil
      party = pl.map { |sp| DemoRun.mon(sp, 50, [:TACKLE]) }
      DemoRun.battle("pp_#{@current}", party, :turns => 1) do
        $game_temp.clear_battle_rules
        setBattleRule("field", id)
        setBattleRule("fieldStage", st) if st > 1
        if foe.length > 1
          setBattleRule("double")
          WildBattle.start(foe[0], 50, foe[1], 50)
        else
          WildBattle.start(foe[0], 50)
        end
      end
      DemoRun.every = 100000
      DemoRun.log("placement #{@current}: #{@done ? 'ok' : 'NO SHOT'}")
    end
  end

  # lowest / highest opaque rows of a bitmap, and the x extent of its lowest 6 opaque rows
  def scan(bmp)
    w, h = bmp.width, bmp.height
    feet = nil
    (h - 1).downto(0) do |y|
      x = 0
      while x < w
        if bmp.get_pixel(x, y).alpha > 40
          feet = y
          break
        end
        x += 1
      end
      break if feet
    end
    return [-1, -1, -1, -1] if !feet
    top = nil
    0.upto(h - 1) do |y|
      x = 0
      while x < w
        if bmp.get_pixel(x, y).alpha > 40
          top = y
          break
        end
        x += 1
      end
      break if top
    end
    l, r = w, -1
    [feet - 5, 0].max.upto(feet) do |y|
      w.times do |x|
        next if bmp.get_pixel(x, y).alpha <= 40
        l = x if x < l
        r = x if x > r
      end
    end
    [feet, l, r, top]
  end

  def intro_log(shot)
    scene = DemoRun.scene
    return if !scene || !scene.respond_to?(:sprites) || !scene.sprites
    room = scene.sprites["battlebg"]
    return if !room || !room.respond_to?(:battler)
    bg = room.instance_variable_get(:@sprites)["bg"]
    return if !bg || bg.disposed?
    @intro_tsv ||= begin
      f = "Captures/placement/intro_#{@current}.tsv"
      File.write(f, %w[shot bg_x bg_y bg_ox bg_oy bg_zx bg_zy v0 x0 y0 oy0 z0 v1 x1 y1 oy1 z1].join("\t") + "\n")
      f
    end
    row = [shot, bg.x.round(2), bg.y.round(2), bg.ox.round(2), bg.oy.round(2), bg.zoom_x.round(4), bg.zoom_y.round(4)]
    [0, 1].each do |i|
      s = scene.sprites["pokemon_#{i}"]
      if s && !s.disposed?
        row += [s.visible ? 1 : 0, s.x.round(2), s.y.round(2), s.oy, s.zoom_y.round(4)]
      else
        row += [0, 0, 0, 0, 0]
      end
    end
    File.open(@intro_tsv, "a") { |f| f.puts(row.join("\t")) }
  rescue StandardError
  end

  def probe(scene, view)
    room = scene.sprites["battlebg"]
    bg = room.instance_variable_get(:@sprites)["bg"]
    (0...scene.battle.battlers.length).each do |i|
      spr = scene.sprites["pokemon_#{i}"]
      next if !spr || spr.disposed?
      anc = room.battler(i)
      bmp = spr.bitmap
      feet, l, r, top = scan(bmp)
      sp = (scene.battle.battlers[i].displaySpecies rescue "?")
      sh = spr.instance_variable_get(:@shadow)
      row = [@current, view, i, sp, anc.x.round(2), anc.y.round(2), spr.x.round(2), spr.y.round(2), spr.ox, spr.oy,
             spr.zoom_x.round(4), spr.zoom_y.round(4), bmp.width, bmp.height, feet, l, r, top,
             bg.x.round(2), bg.y.round(2), bg.ox.round(2), bg.oy.round(2), bg.zoom_x.round(4), bg.zoom_y.round(4),
             (sh && sh.visible) ? 1 : 0]
      bmp.dispose
      File.open(@tsv, "a") { |f| f.puts(row.join("\t")) }
    end
  end

  def shoot(scene, view)
    probe(scene, view)
    base = "Captures/placement/#{@current}_#{view}"
    Graphics.screenshot("#{base}.png")
    hidden = []
    scene.sprites.each do |k, s|
      next if !k.to_s.start_with?("dataBox") || !s || s.disposed? || !s.visible
      s.visible = false
      hidden << s
    end
    2.times { scene.pbUpdate }
    Graphics.screenshot("#{base}_clean.png")
    hidden.each { |s| s.visible = true }
  end

  def hold_and_shoot(scene)
    return if @done || !@current
    @done = true
    (ENV["PP_WAIT"] || 150).to_i.times { scene.pbUpdate }
    DemoRun.every = 100000
    shoot(scene, "main")
    return if ENV["PP_VECTORS"] != "1"
    [[:ENEMY, "enemy"], [:SENDOUT, "sendout"], [:PLAYER, "player"]].each do |vec, tag|
      v = EliteBattle.get_vector(vec, scene.battle) rescue nil
      next if !v
      scene.vector.set(v)
      60.times { scene.pbUpdate }
      shoot(scene, tag)
    end
    scene.vector.reset
    20.times { scene.pbUpdate }
  end
end

if ENV["DEMO_PLAN"].to_s == "placement"
  # PP_GROUND=0: EBDX's own species metrics (the Bridge's feet-on-the-base grounding off), for "before" shots
  if ENV["PP_GROUND"] == "0" && defined?(PrismfallEBDX::GROUND_SPRITES)
    PrismfallEBDX.send(:remove_const, :GROUND_SPRITES)
    PrismfallEBDX.const_set(:GROUND_SPRITES, false)
  end
  # PP_FOOT="16,-2" / PP_RAISE=0: an earlier foot line / player point, for "before" shots of the Bridge's own tuning
  if ENV["PP_FOOT"] && defined?(PrismfallEBDX::FOOT_LINE)
    f, b = ENV["PP_FOOT"].split(",").map(&:to_i)
    PrismfallEBDX::FOOT_LINE[:front] = f
    PrismfallEBDX::FOOT_LINE[:back] = b
  end
  # PP_ROOM_RAISE=0: ignore the rooms' own :player_raise (shots of the art before it existed)
  if ENV["PP_ROOM_RAISE"] == "0" && PrismfallEBDX.respond_to?(:room_player_raise)
    PrismfallEBDX.define_singleton_method(:room_player_raise) { |*_a| 0 }
  end
  if ENV["PP_RAISE"] && defined?(PrismfallEBDX::PLAYER_RAISE)
    PrismfallEBDX.send(:remove_const, :PLAYER_RAISE)
    PrismfallEBDX.const_set(:PLAYER_RAISE, ENV["PP_RAISE"].to_i)
  end

  class << DemoRun
    alias pp_orig_run run unless method_defined?(:pp_orig_run)
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("placement probe boot ok")
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
      PlacementProbe.run_all
      log("done")
    end
  end

  class << DemoRun
    alias pp_tick tick unless method_defined?(:pp_tick)
    def tick
      before = @shots
      pp_tick
      PlacementProbe.intro_log(@shots - 1) if @rec && @shots > before
    end
  end

  module PBDayNight
    class << self
      def isNight?(*a);   false; end
      def isEvening?(*a); false; end
      def isMorning?(*a); false; end
      def isDay?(*a);     true; end
    end
  end

  class Battle
    alias pp_pbCommandPhase pbCommandPhase unless method_defined?(:pp_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        PlacementProbe.hold_and_shoot(@scene)
        @decision = 3
        return
      end
      pp_pbCommandPhase
    end
  end
end
