#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 13 "Behind the Glass", key events in the real engine.
# Antumbra and Lucent aren't built; scenes are staged on built maps with the chapter's real lines:
#   A  Mirror Mere: Dask's rule and "Look back?" (the Glassed Orchard, 522)
#   B  Gym 12: Ilsa, Mindscape, Mega Slowbro        C  the Mindscape: the PC's first line (Saltmere Old Town, 147)
#   D  the tribunal and Kroll unmasked, Mega Sharpedo (Briar Hall's Great Hall, 286)
#   E  the Fault: Rowan or Marchetti                 F  dawn: the Secret Articles; END OF ACT III
#   DEMO_PLAN=ch13   CK_SEGS=ABCDEF   CK_EVERY=4
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch13")
  module Ch13Cap
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
    def self.wait(n); n.times { Graphics.update; $scene.miniupdate rescue nil }; end
    def self.party
      [DemoRun.mon(:LUXRAY, 59, [:WILDCHARGE, :ICEFANG, :CRUNCH, :VOLTSWITCH], :LIFEORB),
       DemoRun.mon(:SCEPTILE, 59, [:LEAFSTORM, :GIGADRAIN, :DRAGONPULSE, :FOCUSBLAST], :MIRACLESEED),
       DemoRun.mon(:LUCARIO, 58, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:GARCHOMP, 59, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:MAMOSWINE, 58, [:ICICLECRASH, :EARTHQUAKE, :ICESHARD, :ROCKSLIDE], :NEVERMELTICE),
       DemoRun.mon(:HYDREIGON, 58, [:DARKPULSE, :DRACOMETEOR, :FLAMETHROWER, :ROOST], :LEFTOVERS)]
    end
  end

  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch13 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch13Cap.party
      12.times { |i| $player.badges[i] = true }
      segs = (ENV["CK_SEGS"] || "ABCDEF").upcase

      if segs.include?("A")
        Ch13Cap.goto(522, 20, 20, Tone.new(-30, -40, 20, 40), "Glass Veil")
        Ch13Cap.scene("ch13_A_mere") do
          Ch13Cap.say(["(A lake so still it isn't a lake. Halfway across, the reflection stops matching: in the water, the far shore has a city on it.)",
                       "Dask: Welcome, behind. Behind, welcome.",
                       "Dask: One rule. Only one. Never look back through the Glass once you've crossed.",
                       "Dask: Once you're behind, you're behind. I said it twice. Remember that I said it twice.",
                       "\\pf[JUNO,panic]???: \\PN! \\PN, wait! It's me! I came the long way— wait for me! Please!"])
          pbMessage("(Her voice exactly.)", ["Look back", "Keep walking"], 2, nil, 1)
          Ch13Cap.say(["(The voice calls twice more, then stops in the middle of your name.)"])
        end
      end

      if segs.include?("B")
        Ch13Cap.goto(147, 20, 20, Tone.new(0, 0, 0, 0), "Saltwife")
        Ch13Cap.scene("ch13_B_ilsa_msgs") do
          Ch13Cap.say(["Ilsa: You're thinking very loudly. Please stop.",
                       "Ilsa: The truth is a weapon. I've kept it sheathed for eleven years. Don't mistake that for mercy. Shall we?"])
        end
        DemoRun.battle("ch13_B_ilsa", Ch13Cap.party, turns: (ENV["CK_BT"] || 6).to_i) do
          Prismfall.gym_battle(12, can_lose: true, double: false)
        end
      end

      if segs.include?("C")
        Ch13Cap.goto(147, 20, 20, Tone.new(60, 50, 30, 0), "Saltwife")
        Ch13Cap.scene("ch13_C_mindscape") do
          Ch13Cap.say(["(Bells. Festival banners in eighteen colours. Lower Crownhaven, AF 290. Everything a little too bright, like a memory of a summer.)",
                       "(A child of five on the chapel steps, holding a Choir ribbon. They have your face.)",
                       "Child: Mum's singing. Do you want to see the light?",
                       "Child: It's going to hurt."])
          pbMessage("(The child waits.)", ["\"Show me.\"", "\"I'm scared too.\"", "\"...Not yet.\""], 3, nil, 1)
          Ch13Cap.say(["\\pf[PLAYER,sad]\\PN: I'm scared too.",
                       "Child: I know. That's why I waited for you.",
                       "(A choir singing one long note in eighteen voices. Behind the loft, where no one can see: brass machines, each with a little gold sunburst.)"])
          $game_screen.start_flash(Color.new(255, 255, 255, 255), 30) rescue nil
          $game_screen.start_shake(6, 9, 30) rescue nil
          Ch13Cap.wait(40)
          Ch13Cap.say(["(A crack. Light. Something small and sharp goes into the child's chest.)",
                       "(A woman in a black Ghost Warden's veil throws herself over the child.)",
                       "Voice: Find the child.",
                       "Ilsa: (very quietly) The man in white was my father."])
        end
      end

      if segs.include?("D")
        Ch13Cap.goto(286, 15, 15, Tone.new(-10, -10, 0, 10), nil)
        Ch13Cap.scene("ch13_D_tribunal_msgs") do
          Ch13Cap.say(["Clerk of the Court: The Accord's tribunal is in session. The Sovereign presides.",
                       "Rowan: I wanted to pull the nails. I was wrong about how. I was not wrong about why.",
                       "Kaito: Marrowgate. Fifteen years ago. My orders. My unit. I sealed the gate. They were still knocking.",
                       "Ilsa: Sable is Sabine Kroll. Meridian Special Accounts. She cracked Lumen's Plate. On orders.",
                       "Kroll: Light for everyone, right? ...Oh, never mind. You're no fun any more, Provost."])
        end
        DemoRun.battle("ch13_D_kroll", Ch13Cap.party, turns: (ENV["CK_DT"] || 7).to_i) do
          setBattleRule("field", :MINDSCAPE); setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_KROLL, "Sabine")
        end
      end

      if segs.include?("E")
        Ch13Cap.goto(286, 15, 15, Tone.new(-80, -80, -40, 60), nil)
        Ch13Cap.scene("ch13_E_fault") do
          Ch13Cap.say(["(The water in the court's carafes shivers. Then the benches. Then the floor.)"])
          $game_screen.start_shake(9, 9, 90) rescue nil
          Ch13Cap.wait(60)
          Ch13Cap.say(["(The dome cracks in one long line, then a hundred, and comes down in a slow, glittering rain. The floor gives way into the flooded undercroft.)",
                       "(Rowan, chained in the dock, the water at his chest. Marchetti, pinned under the orrery's brass ring. You can reach one.)"])
          pbMessage("(The water's still rising.)", ["Break Rowan's chain", "Heave the ring off Marchetti"], 2, nil, 0)
          Ch13Cap.say(["Rowan: Ask the Drowned Crown. It's awake now. So are you."])
        end
      end

      if segs.include?("F")
        Ch13Cap.goto(147, 20, 20, Tone.new(-20, -20, 10, 30), "Saltwife")
        Ch13Cap.scene("ch13_F_dawn") do
          Ch13Cap.say(["Ilsa: Father's Secret Articles. The parts the Accord doesn't teach. Don't read them yet.",
                       "Ilsa: Go and find Bastian Ore first. He was there.",
                       "(In every broken pane of glass, six black wings fold, and unfold, and fold.)",
                       "IV — The Drowned Crown"])
        end
      end
      log("done")
    end
  end
end
