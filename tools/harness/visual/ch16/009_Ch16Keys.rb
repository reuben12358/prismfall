#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 16 "Clear Air": key events in the real engine.
# Cogsworth isn't built. The scenes are staged on built Lumen maps with the chapter's real lines:
#   A the Unity Rally and Rook (180)   B Gym 15 Magnus   C the casting floor: PC + Rook vs Marchetti + Quent
#   D the blueprints (193)   E Zekrom   F Magnus and Operation Clear Air   G Interlude IV (181)   H the supply-lift
#   DEMO_PLAN=ch16   CK_SEGS=ABCDEFGH   CK_EVERY=4
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch16")
  module Ch16Cap
    def self.say(lines); lines.each { |l| pbMessage(l) }; end
    def self.scene(name)
      DemoRun.record(name); DemoRun.auto = true
      begin
        yield
      rescue Exception => e
        raise if e.is_a?(SystemExit)
        DemoRun.log("EXCEPTION #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(15).join("\n  "))
      end
      20.times { Graphics.update; $scene.miniupdate rescue nil }
      DemoRun.auto = false; DemoRun.stop
    end
    def self.goto(map, x, y, tone, near = nil)
      $game_map.setup(map)
      ev = near && $game_map.events.values.find { |e| e.name == near }
      x, y = ev.x, ev.y + 2 if ev
      DemoRun.log("goto #{map} near #{near.inspect}: #{ev ? 'found' : 'not found'} -> #{x},#{y}")
      $game_player.moveto(x, y); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_screen.start_tone_change(tone, 0) rescue nil
      20.times { Graphics.update; $scene.miniupdate }
    end
    def self.tone(t, d = 20); $game_screen.start_tone_change(t, d) rescue nil; wait(d + 2); end
    def self.flash(c, d = 24); $game_screen.start_flash(c, d) rescue nil; wait(d + 6); end
    def self.wait(n); n.times { Graphics.update; $scene.miniupdate rescue nil }; end
    def self.party(lv = 66)
      [DemoRun.mon(:SCEPTILE, lv, [:LEAFSTORM, :GIGADRAIN, :DRAGONPULSE, :FOCUSBLAST], :MIRACLESEED),
       DemoRun.mon(:LUXRAY, lv, [:WILDCHARGE, :ICEFANG, :CRUNCH, :VOLTSWITCH], :LIFEORB),
       DemoRun.mon(:LUCARIO, lv, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:GARCHOMP, lv, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:AGGRON, lv, [:IRONHEAD, :HEAVYSLAM, :EARTHQUAKE, :STONEEDGE], :AGGRONITE),
       DemoRun.mon(:VAPOREON, lv, [:SCALD, :ICEBEAM, :WISH, :PROTECT], :LEFTOVERS)]
    end
  end

  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch16 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch16Cap.party(70)
      14.times { |i| $player.badges[i] = true }
      $bag.add(:MEGARING) rescue nil
      segs = (ENV["CK_SEGS"] || "ABCDEFGH").upcase
      night = Tone.new(-60, -60, -30, 60)

      if segs.include?("A")
        Ch16Cap.goto(180, 20, 20, Tone.new(-20, -25, -10, 70), "Meridian Spire")
        Ch16Cap.scene("ch16_A_rally") do
          Ch16Cap.say(["(Cogsworth. Three shifts, and the shift-whistles never quite stop. On a giant screen, Aurelian Voss fills the sky.)",
                       "Voss (screen): Order. Light. Unity. Every rivet you set this shift is a child who never turns to glass.",
                       "Worker: Don't know what we're building. Big, whatever it is. Round. Eighteen of something.",
                       "(The canteen. At the back, alone, unshaven, no drone: Rook Calder.)",
                       "Rook: I'm off-camera. I haven't been off-camera since I was fourteen. How do people eat when nobody's watching?",
                       "Rook: Sable. With a Meridian keycard. The night of the Lowlight. I've had it for months. I was scared."])
          pbMessage("Rook: Put it out now? Or wait for the worst possible moment?", ["Leak it now", "Hold it for the Festival"], 2, nil, 1)
          Ch16Cap.say(["Rook: The worst possible moment. Opening ceremony. I can do that. I'm good at moments."])
        end
      end

      if segs.include?("B")
        DemoRun.battle("ch16_B_magnus", Ch16Cap.party(70), turns: (ENV["CK_BT"] || 8).to_i) do
          Prismfall.gym_battle(15, can_lose: true)
        end
      end

      if segs.include?("C")
        15.times { |i| $player.badges[i] = true }
        DemoRun.battle("ch16_C_casting", Ch16Cap.party(70), turns: 7) do
          pbRegisterPartner(:LEADER_ROOK, "Rook", 16)
          setBattleRule("field", :FACTORY)
          setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene", 2, :MERIDIAN_QUENT, "Percival", 1)
          pbDeregisterPartner rescue nil
        end
      end

      if segs.include?("D")
        Ch16Cap.goto(193, 15, 15, Tone.new(-40, -40, -20, 80), "Plate cradle")
        Ch16Cap.scene("ch16_D_blueprints") do
          Ch16Cap.say(["(The Drafting Vault. One blueprint across a table as long as a ship: a ring of eighteen locks built into a new arena.)",
                       "(A margin note: \"Keystone. To be recovered from site AURELIA.\")",
                       "(At the bottom of the sheet, the box for the load it's built to carry.)"])
          Ch16Cap.flash(Color.new(255, 255, 255, 120), 10)
          Ch16Cap.say(["CALIBRATION SUBJECT: UNIMPRINTED-01. RETENTION: INDEFINITE.",
                       "(You read it twice. It doesn't change.)",
                       "Rook: \"Unimprinted\"... that's you. What's \"retention\"?"])
          pbMEPlay("Key item get") rescue nil
          pbMessage("\\me[Key item get]You obtained the Arbiter Blueprints!") rescue nil
        end
      end

      if segs.include?("E")
        Ch16Cap.goto(193, 15, 15, Tone.new(-30, -30, 0, 60), "Plate cradle")
        Ch16Cap.scene("ch16_E_core") do
          Ch16Cap.say(["(A great black stone, split open like an egg. Half out of it, a black dragon bound in golden cable, a hundred strands humming.)",
                       "(It isn't asking you to fight it. It's asking you to help it pull.)"])
        end
        DemoRun.battle("ch16_E_zekrom", Ch16Cap.party(71), turns: 18) do
          Prismfall::Bosses.wild_battle(:ZEKROM_ENGINE, :can_lose => true)
        end
        log("zekrom result #{(Prismfall::Bosses.last_result || {})[:result].inspect}")
      end

      if segs.include?("F")
        Ch16Cap.goto(193, 15, 15, Tone.new(-50, -50, -30, 90), "Plate cradle")
        Ch16Cap.scene("ch16_F_magnus") do
          Ch16Cap.say(["(The vault, wrecked. Rain through the hole Zekrom tore. Smoothing a wet sheet with his steel hand: Magnus Strade.)",
                       "Magnus: Don't run. I haven't called security. I'm not going to.",
                       "Magnus: I don't build weapons. I build tolerances. I learned the truth two years ago. I kept building. The mathematics was beautiful.",
                       "Magnus: I didn't know it was a child until I saw you in the gym.",
                       "(He winds his pocket watch. Click, click, click.)"])
          pbMessage("Magnus: What will you do with me?", ["Expose him", "Appeal to his conscience"], 2, nil, 2)
          Ch16Cap.say(["(You hold up the sheet with your designation on it. The question is on the paper.)",
                       "Magnus: ...Will I let it take a child."])
        end
        Ch16Cap.goto(180, 20, 20, night, "Meridian Spire")
        Ch16Cap.scene("ch16_F_clearair") do
          Ch16Cap.say(["(On every screen in Cogsworth, a white sunburst on black, and two words: OPERATION CLEAR AIR.)",
                       "Voss (screen): Tonight the Directorate restores order to the Underveil and the Mirefen. Go home. Sleep.",
                       "Worker: My mum lives down there."])
        end
      end

      if segs.include?("G")
        Ch16Cap.goto(181, 20, 20, Tone.new(-70, -60, -50, 100), nil)
        Ch16Cap.scene("ch16_G_interlude") do
          Ch16Cap.say(["INTERLUDE IV — Clear Air",
                       "(Corvin's Infirmary in the Mirefen. Night. Rain on the tin roof. Behind a bead curtain, the Quiet Ward: forty patients, dreaming.)",
                       "Wenlow: Right! Evening rounds! Mrs. Pell, water. Old Fisk, the green one, not the brown one.",
                       "Radio: Infirmary? Grey coats at the east walks. They're going house to house. They've got the Sweetrot list.",
                       "Wenlow: ...Okay. Okay. I've read the book twice.",
                       "Wenlow: They won't search the glass ones. Nobody ever looks at the glass ones.",
                       "Lieutenant: Medical facility. We have reason to believe Sweetrot users are being harboured on these premises.",
                       "Wenlow: This is a hospital.",
                       "Wenlow: You have to —"])
          Ch16Cap.tone(Tone.new(-255, -255, -255, 0), 0)
          Ch16Cap.wait(80)
        end
      end

      if segs.include?("H")
        Ch16Cap.goto(181, 20, 20, Tone.new(-10, -20, -30, 120), nil)
        Ch16Cap.scene("ch16_H_lift") do
          Ch16Cap.say(["(Dawn. Rook at the supply-lift, holding the cage door.)",
                       "Rook: I heard on the union band. The Mirefen. The Infirmary. A kid.",
                       "(The cage goes down. Far below, over the Underveil, smoke, rising straight up in the still morning air.)"])
        end
      end
      log("done")
    end
  end
end
