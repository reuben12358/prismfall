#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Ch19 "the lines" (story/38_SCRIPT_CH19.md, V140 5 -> 6) on the built
# war maps: for each :war_climax side, the map's own events run - the "War front" sets S605-607, the gauntlet singles
# and the partner double start from their events - and every battle is auto-won after a few frames.
#   DEMO_PLAN=warlines   WL_SIDES=back_ashkaar,back_isenmar,stand_between   WL_SHOTS=1 (every 30th frame; off by default)
# Per side: the player stands in the partner pair's line of sight (one step away), so the Trainer(4) page must start by
# sight; if it doesn't within 400 frames the event is started directly (logged as "sight: no").
# Copy maps_out/Data/system_prismfall.txt and the rebuilt Map920/924/925/926.rxdata into run_intro's game/Data first.
# RESULT lines in demo.log: each battle's foes, its field, the partner, and after the double pfm(:war_partner_done),
# V140, the pair's self-switch A, and whether 926's crest still holds any trainer.
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("warlines")
  module WarLines
    SIDES = { :back_ashkaar => [920, "Sigrun"], :back_isenmar => [924, "Marisol"], :stand_between => [925, "Sigrun"] }
    @battles = []
    class << self; attr_accessor :battles; end

    def self.wait(n); n.times { Graphics.update; Input.update; $scene.update }; end

    def self.goto(map, x, y, dir)
      $game_map.setup(map)
      $game_player.moveto(x, y)
      { :left => 4, :right => 6, :up => 8, :down => 2 }[dir].then { |d| $game_player.direction = d }
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      wait(10)
    end

    # The pair: the Trainer(4) event whose pages call pbRegisterPartner. Returns [event, the tile one step out of its
    # line of sight, the direction to step in].
    def self.pair
      ev = $game_map.events.values.find do |e|
        e.name == "Trainer(4)" && e.instance_variable_get(:@event).pages.any? { |pg| pg.list.any? { |c| c.parameters.to_s.include?("pbRegisterPartner") } }
      end
      return nil if !ev
      dx, dy = { 2 => [0, 1], 4 => [-1, 0], 6 => [1, 0], 8 => [0, -1] }[ev.direction]
      # stand 4 tiles out (just outside sight 4 would be 5): step once toward the pair from 5 out
      [ev, ev.x + dx * 5, ev.y + dy * 5, { [0, 1] => :up, [-1, 0] => :right, [1, 0] => :left, [0, -1] => :down }[[dx, dy]]]
    end

    def self.run_side(side)
      map, partner = SIDES[side]
      Prismfall::Narrative.store[:choices][:war_climax] = side   # one save, three sides: set it directly
      PrismfallMaps.flags.delete(:war_partner_done) rescue nil
      $game_variables[140] = 5
      goto(map, 1, 1, :down)   # somewhere harmless while the War front (parallel, every 60 frames) sets S605-607
      wait(80)
      front = [605, 606, 607].map { |i| $game_switches[i] }
      DemoRun.log("#{side}: the War front set S605-607 = #{front.inspect}")
      [605, 606, 607].zip([:back_ashkaar, :back_isenmar, :stand_between]).each { |i, c| $game_switches[i] = (c == side) }
      $game_map.need_refresh = true
      wait(2)
      $game_map.refresh
      ev, sx, sy, dir = pair   # after the refresh: the pair's own page (and its facing) is active
      if !ev
        DemoRun.log("RESULT #{side}: map #{map} has no partner pair event")
        return
      end
      raw = ev.instance_variable_get(:@event)
      raw.pages.each_with_index do |pg, i|
        c = pg.condition
        DemoRun.log("  page #{i}: sw1=#{c.switch1_valid}/#{c.switch1_id} self=#{c.self_switch_valid}/#{c.self_switch_ch} trig=#{pg.trigger} " \
                    "cmds=#{pg.list.length} gfx=#{pg.graphic.character_name}/#{pg.graphic.direction} active=#{ev.instance_variable_get(:@page).equal?(pg)}")
      end
      $game_player.moveto(sx, sy)
      $game_player.direction = { :left => 4, :right => 6, :up => 8, :down => 2 }[dir]
      wait(10)
      DemoRun.log("#{side}: map #{map} S605=#{$game_switches[605]} S606=#{$game_switches[606]} S607=#{$game_switches[607]} " \
                  "pair at #{ev.x},#{ev.y} dir #{ev.direction} page=#{ev.instance_variable_get(:@page) ? 'on' : 'off'} player #{sx},#{sy}")
      before = WarLines.battles.length
      DemoRun.auto = true
      { :up => 8, :down => 2, :left => 4, :right => 6 }[dir].then { |d| $game_player.move_generic(d) rescue $game_player.send({ 8 => :move_up, 2 => :move_down, 4 => :move_left, 6 => :move_right }[d]) }
      sight = false
      400.times do
        wait(1)
        if $game_system.map_interpreter.running? || $game_temp.in_battle
          sight = true
          break
        end
      end
      ev.start if !sight
      frames = 0
      loop do
        wait(1); frames += 1
        break if frames > 3000
        break if WarLines.battles.length > before && !$game_system.map_interpreter.running? && !$game_temp.in_battle && frames > 60
      end
      DemoRun.auto = false
      selfA = $game_self_switches[[map, ev.id, "A"]]
      DemoRun.log("[#{Time.now.strftime('%H:%M:%S')}] RESULT #{side} (map #{map}): sight: #{sight ? 'yes' : 'no'}; battles #{WarLines.battles[before..].inspect}; " \
                  "war_partner_done=#{pfm?(:war_partner_done).inspect} V140=#{$game_variables[140]} pair_selfA=#{selfA.inspect} " \
                  "partner_left=#{$PokemonGlobal.partner.inspect} expected partner #{partner}")
    end

    def self.crest
      $game_map.setup(926)
      tr = $game_map.events.values.select { |e| e.name =~ /trainer\(/i || e.name == "Partner" }.map { |e| [e.name, e.x, e.y] }
      leg = $game_map.events.values.find { |e| e.name == "The legend" }
      DemoRun.log("RESULT 926: trainer/partner events left #{tr.inspect}; the legend at #{leg && [leg.x, leg.y].inspect}")
    end
  end

  class << DemoRun
    # The packaged game names switches and variables from Data/system_prismfall.txt (tools/package.sh); Essentials'
    # switchIsOn? treats an unnamed switch as off, so the war maps' S605-607 pages need the names.
    def wl_names
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
      log("warlines capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      wl_names
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 2; $PokemonSystem.battlescene = 1
      Prismfall.record_starter(:SCEPTILE) rescue nil
      17.times { |i| $player.badges[i] = true }
      # Lv 85 = the cap at 17 badges: no EXP, so no move-learning prompt stalls the auto-won battles.
      $player.party = [DemoRun.mon(:SCEPTILE, 85, [:LEAFSTORM, :GIGADRAIN, :DRAGONPULSE, :FOCUSBLAST]),
                       DemoRun.mon(:LUCARIO, 85, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE]),
                       DemoRun.mon(:VAPOREON, 85, [:SCALD, :ICEBEAM, :WISH, :PROTECT])]
      self.every = 30
      record("ch19_warlines") if ENV["WL_SHOTS"] == "1"
      (ENV["WL_SIDES"] || "back_ashkaar,back_isenmar,stand_between").split(",").each do |s|
        begin
          WarLines.run_side(s.strip.to_sym)
        rescue Exception => e
          raise if e.is_a?(SystemExit)
          log("EXCEPTION #{s}: #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(12).join("\n  "))
        end
      end
      WarLines.crest
      stop
      log("done")
    end
  end
  module Input
    class << self
      alias wl_trigger? trigger? unless method_defined?(:wl_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return wl_trigger?(button)
      end
    end
  end
  class Battle
    alias wl_pbCommandPhase pbCommandPhase unless method_defined?(:wl_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        foes = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        allies = (@player || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        fld = (field_effect rescue nil)
        fld = (fld.respond_to?(:id) ? fld.id : fld)
        DemoRun.log("[#{Time.now.strftime('%H:%M:%S')}] battle vs #{foes.join(' + ')} field=#{fld.inspect} side=#{allies.join(' + ')} double=#{pbSideSize(0) > 1}")
        WarLines.battles << { :foes => foes, :field => fld, :side => allies }
        if ENV["WL_DIAG"] == "1"
          DemoRun.every = 120
          DemoRun.record("ch19_warlines_diag")
        end
        30.times { @scene.pbUpdate rescue Graphics.update }
        @decision = 1
        return
      end
      wl_pbCommandPhase
    end

    alias wl_pbEndOfBattle pbEndOfBattle unless method_defined?(:wl_pbEndOfBattle)
    def pbEndOfBattle
      DemoRun.log("  [#{Time.now.strftime('%H:%M:%S')}] end of battle: decision #{@decision}") if DemoRun.auto
      ret = wl_pbEndOfBattle
      DemoRun.log("  end of battle done") if DemoRun.auto
      ret
    end
  end
  class Battle::Scene
    alias wl_pbDisplayPausedMessage pbDisplayPausedMessage unless method_defined?(:wl_pbDisplayPausedMessage)
    def pbDisplayPausedMessage(msg, &block)
      DemoRun.log("  paused: #{msg}") if DemoRun.auto
      wl_pbDisplayPausedMessage(msg, &block)
    end
    alias wl_pbEndBattle pbEndBattle unless method_defined?(:wl_pbEndBattle)
    def pbEndBattle(result)
      DemoRun.log("  scene end battle #{result}") if DemoRun.auto
      ret = wl_pbEndBattle(result)
      DemoRun.log("  scene end battle done") if DemoRun.auto
      ret
    end
  end
end
