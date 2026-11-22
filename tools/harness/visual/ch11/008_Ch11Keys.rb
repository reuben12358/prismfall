#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 11 "The Thaw", key events in the real engine.
# Rimeholt isn't built yet, so the overworld beats are staged on the Frostflat Causeway (map 560, a
# frozen causeway) with the chapter's real lines; the battles are the real Ch11 battles:
#   A  Frostfang: "Those aren't caravans" and the :war_warning choice box
#   B  the Thaw partner battle: PC + Juno (rival battle 5) vs Directorate Ostrander + Vell,
#      :FROZEN_LAKE turning to :WATER_SURFACE by the scripted fieldChange rule at round 2
#   C  "The lake breathes": the GO_WEATHER prompt
#   D  Kyogre (KYOGRE_ISENMAR), multi-bar boss, AI vs AI
#   E  the Ebbmouth Strike: PC + Marisol vs the Strikebreaker + Foreman
#   DEMO_PLAN=ch11   CK_SEGS=ABCDE (subset)   CK_EVERY=3
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch11")
  module Ch11Cap
    def self.say(lines)
      lines.each { |l| pbMessage(l) }
    end

    def self.scene(name)
      DemoRun.record(name)
      DemoRun.auto = true
      begin
        yield
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        DemoRun.log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(15).join("\n  "))
      end
      20.times { Graphics.update; $scene.miniupdate rescue nil }
      DemoRun.auto = false
      DemoRun.stop
    end

    def self.party
      [DemoRun.mon(:RAICHU, 54, [:THUNDERBOLT, :GRASSKNOT, :NASTYPLOT, :FOCUSBLAST], :LIFEORB),
       DemoRun.mon(:SCEPTILE, 54, [:LEAFSTORM, :GIGADRAIN, :DRAGONPULSE, :FOCUSBLAST], :MIRACLESEED),
       DemoRun.mon(:LUCARIO, 53, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:ROTOM, 53, [:THUNDERBOLT, :SHADOWBALL, :VOLTSWITCH, :WILLOWISP], :LEFTOVERS),
       DemoRun.mon(:ARCANINE, 53, [:FLAREBLITZ, :WILDCHARGE, :EXTREMESPEED, :MORNINGSUN], :SITRUSBERRY),
       DemoRun.mon(:GARCHOMP, 54, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE], :SITRUSBERRY)]
    end
  end

  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch11 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 1
      $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 3).to_i
      $player.party = Ch11Cap.party
      10.times { |i| $player.badges[i] = true }   # badge 10: the level cap is 55, as after Gym 10
      $game_map.setup(560)
      $game_player.moveto(20, 20)
      $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      30.times { Graphics.update; $scene.miniupdate }
      segs = (ENV["CK_SEGS"] || "ABCDE").upcase

      if segs.include?("A")
        Ch11Cap.scene("ch11_A_frostfang") do
          Ch11Cap.say([
            "(North-east, beyond the Mast Glacier, a line of thin grey threads going straight up. Over them, a slow ring of black specks, turning.)",
            "\\pf[JUNO,neutral]Juno: Are those chimneys? There's no town out there.",
            "\\pf[JUNO,shocked]Juno: Those aren't caravans, are they.",
            "Bryn: Cookfires. Four days now. That's Ossarian sand. Ashkaar's got no business on it unless somebody let them."])
          pbMessage("\\pf[JUNO,neutral]Juno: I could send it on the Circular. Or you could tell them. Or... nobody.",
                    ["Tell Isenmar", "Tell Ashkaar they've been seen", "Juno sends it to everyone", "Say nothing"], 4, nil, 2)
          Ch11Cap.say(["\\pf[JUNO,neutral]Juno: Everyone gets it. If anyone's going to start a war, they'll have to start it knowing everyone saw them come."])
        end
      end

      if segs.include?("B")
        $game_screen.start_tone_change(Tone.new(-80, -70, -20, 40), 0) rescue nil
        Ch11Cap.scene("ch11_B_thaw_msgs") do
          Ch11Cap.say([
            "Pell: DRAW 141%... 148%... 155%. The ice load sensor stopped answering an hour ago.",
            "\\pf[JUNO,angry]Juno: I'm a Warden. That's authorisation. WAKE THE CITY.",
            "(The ice cracks. Not like a window. Like a page tearing, slow, all the way across the harbour.)",
            "Directorate Officer: Lattice asset recovery. Step back, or be stepped back.",
            "\\pf[JUNO,angry]Juno: There are people in the WATER. \\PN. With me."])
        end
        DemoRun.battle("ch11_B_partner_battle", Ch11Cap.party, turns: 6) do
          pbRegisterPartner(:RIVAL_JUNO, "Juno", Prismfall::Rival.version_for(5))
          setBattleRule("field", :FROZEN_LAKE)
          setBattleRule("fieldChange", [2, :WATER_SURFACE, "The ice under the battlefield gives way!"])
          setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Ostrander", 11, :MERIDIAN_DIRECTORATE, "Vell", 11)
          pbDeregisterPartner rescue nil
        end
      end

      if segs.include?("C")
        Ch11Cap.scene("ch11_C_lake_breathes") do
          Ch11Cap.say([
            "(The whole harbour lifts, slowly, like a chest filling. Then it lets out, with a sigh you feel in your teeth.)",
            "(In the black water beyond the second tower, something opens. An eye, bigger than a house.)",
            "(It looks at you.)",
            "Anja: That's not a Pokémon, that's WEATHER. TOWERS! EVERYBODY TO THE TOWERS!"])
          pbMessage("(Anja said run.)", ["Fight it now", "Get to the towers"], 2, nil, 1)
        end
      end

      if segs.include?("D")
        # a party built for Kyogre the way a player would bring one at cap 55 (Water/Ice resists, Volt/Water Absorb)
        kparty = [DemoRun.mon(:LANTURN, 55, [:THUNDERBOLT, :DISCHARGE, :ICEBEAM, :THUNDERWAVE], :LEFTOVERS),
                  DemoRun.mon(:LUDICOLO, 55, [:GIGADRAIN, :ENERGYBALL, :ICEBEAM, :PROTECT], :SITRUSBERRY),
                  DemoRun.mon(:FERROTHORN, 55, [:POWERWHIP, :GYROBALL, :LEECHSEED, :PROTECT], :LEFTOVERS),
                  DemoRun.mon(:TOXTRICITY, 55, [:OVERDRIVE, :BOOMBURST, :SLUDGEBOMB, :VOLTSWITCH], :SITRUSBERRY),
                  DemoRun.mon(:RAICHU, 54, [:THUNDERBOLT, :GRASSKNOT, :NASTYPLOT, :FOCUSBLAST], :LIFEORB),
                  DemoRun.mon(:LUCARIO, 54, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY)]
        kparty.each { |p| p.level = (ENV["CK_KLV"] || 55).to_i; p.calc_stats }
        DemoRun.battle("ch11_D_kyogre", kparty, turns: 18) do
          Prismfall::Bosses.wild_battle(:KYOGRE_ISENMAR, :can_lose => true)
        end
        log("kyogre result #{(Prismfall::Bosses.last_result || {})[:result].inspect}")
      end

      if segs.include?("W")   # GO_WEATHER's Kyogre, as a check only
        DemoRun.battle("ch11_W_weather", Ch11Cap.party, turns: 2) do
          Prismfall::Bosses.wild_battle(:KYOGRE_WEATHER)
        end
        log("weather result #{(Prismfall::Bosses.last_result || {})[:result].inspect}")
      end

      if segs.include?("E")
        $game_screen.start_tone_change(Tone.new(-20, -30, -10, 20), 0) rescue nil
        Ch11Cap.scene("ch11_E_strike_msgs") do
          Ch11Cap.say([
            "(Ebbmouth. A thousand people on the Mill Quay with dockworkers' saws. The Lattice cables screech, and THUNK, and the Ebb runs both ways again.)",
            "Directorate Foreman: By order of the Mandate, disperse, and nobody gets hurt.",
            "Marisol: Nobody gets hurt. You'll want to look at that pole.",
            "Marisol: He was nineteen. Nineteen. Tell me again how the Hollow are the monsters."])
        end
        DemoRun.battle("ch11_E_strike_battle", Ch11Cap.party, turns: 5) do
          pbRegisterPartner(:LEADER_MARISOL, "Marisol", 1)
          setBattleRule("field", :WATER_SURFACE)
          setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_AGENT_M, "Strikebreaker", 11, :MERIDIAN_DIRECTORATE, "Foreman", 11)
          pbDeregisterPartner rescue nil
        end
      end
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
end
