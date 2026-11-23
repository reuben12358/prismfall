#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 15 "The Hollow Cathedral": key events in the real engine.
# Gravenmoor isn't built. The scenes are staged on built maps with the chapter's real lines:
#   A  the War Convoy at the Steamline's edge (925, built)
#   B  Gym 14: Ysolde, double, Hollow Cathedral
#   C  the Cathedral echo: AF 290 through Morwen's eyes (Cathedral of the Evergreen 295, sepia)
#   D  K6: Kestrel, Hollow Cathedral
#   E  Edda at Morwen's grave: Morwen's Ring
#   F  Giratina, Reverse Depths (:INVERSE), Altered -> Origin
#   G  the Hush
#   DEMO_PLAN=ch15   CK_SEGS=ABCDEFG   CK_EVERY=4
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch15")
  module Ch15Cap
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
      log("ch15 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch15Cap.party
      13.times { |i| $player.badges[i] = true }
      $bag.add(:MEGARING) rescue nil
      segs = (ENV["CK_SEGS"] || "ABCDEFG").upcase
      sepia = Tone.new(30, 0, -40, 200)

      if segs.include?("A")
        Ch15Cap.goto(925, 20, 20, Tone.new(10, 0, -10, 40), "Convoy marker")
        Ch15Cap.scene("ch15_A_convoy") do
          Ch15Cap.say(["(Twelve sledges at the Steamline's edge. The caravan-mother turns her camel round.)",
                       "Caravan-mother: Past the glass, the glass is yours.",
                       "(You walk point into the steam. Where you step, the Bleed goes quiet. The sledges follow your footprints exactly.)",
                       "Ashkaar Rider: Halt! Sledges into Skaldfast. Under whose banner?",
                       "Ashkaar Rider: ...Go on. Dominar's orders are \"no arms past the glass\". He never said anything about milk."])
        end
      end

      if segs.include?("B")
        DemoRun.battle("ch15_B_ysolde", Ch15Cap.party(66), turns: (ENV["CK_BT"] || 8).to_i) do
          Prismfall.gym_battle(14, can_lose: true, double: true)
        end
      end

      if segs.include?("C")
        Ch15Cap.goto(295, 20, 20, Tone.new(-50, -60, -40, 60), "Evergreen prior")
        Ch15Cap.scene("ch15_C_echo") do
          Ch15Cap.say(["Ysolde: Kestrel. Not like this. She made me swear — when you were ready —",
                       "Kestrel: Ten years, Ysolde. \"When he's ready.\" I'm ready. Watch me be ready."])
          Ch15Cap.flash(Color.new(255, 255, 255, 200), 16)
          Ch15Cap.tone(sepia, 30)
          Ch15Cap.say(["(Crownhaven's arena, ten years ago, through someone's eyes. Bells. The Choir in white. In the front row, singing: Ines.)",
                       "(Behind the Choir loft: brass machines with dials. Gold sunburst plates. A young man in a white coat leans in to read a dial: Aurelian Voss.)"])
          Ch15Cap.flash(Color.new(255, 255, 255, 255), 30)
          Ch15Cap.say(["(A sound like a bell breaking.)",
                       "(A splinter of colourless light flies out of the Crown and goes into the chest of a child of five in a Choir ribbon.)",
                       "(The eyes run. The Glassfall sweeps the lower stands and forty people turn to glass. She throws herself over the child.)",
                       "Valen: Find the child. Whatever it costs. Find the child."])
          Ch15Cap.tone(Tone.new(-30, -40, -60, 220), 20)
          Ch15Cap.say(["Morwen: Take them. Edda's boat is at the Landing at midnight. I'll carry the name. Go.",
                       "(A Mismagius lays a hand over the sleeping child's eyes, the way you'd close a curtain.)",
                       "Morwen: Kestrel. I'm sorry."])
          Ch15Cap.wait(40)
          Ch15Cap.say(["(And then, impossibly, the echo turns her head. Across ten years. She looks straight at you.)",
                       "Morwen: Little one. You came back. I told her not to let you."])
          Ch15Cap.tone(Tone.new(-50, -60, -40, 60), 40)
          Ch15Cap.say(["Kestrel: My whole life for you. Do you know what they called me in school? The Glassfall boy.",
                       "Kestrel: And she was saving YOU."])
        end
      end

      if segs.include?("D")
        14.times { |i| $player.badges[i] = true }
        DemoRun.battle("ch15_D_k6", Ch15Cap.party(66), turns: (ENV["CK_DT"] || 8).to_i) do
          Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 6, field: :HOLLOW_CATHEDRAL, can_lose: true)
        end
        Ch15Cap.goto(295, 20, 20, Tone.new(-50, -60, -40, 60), "Evergreen prior")
        Ch15Cap.scene("ch15_D_after") do
          pbMessage("(He's on his knees on the altar step. He doesn't look up.)",
                    ["\"I'm sorry. I didn't know.\"", "\"I was five. She chose.\"", "\"Your mother saved my life.\""], 3, nil, 1)
          Ch15Cap.say(["Wren: I was five. She chose. Don't you dare make her choice my crime.",
                       "Kestrel: ...There you are. I wondered if there was anybody in there."])
        end
      end

      if segs.include?("E")
        Ch15Cap.goto(295, 20, 20, Tone.new(-40, -40, -20, 100), "Evergreen prior")
        Ch15Cap.scene("ch15_E_grave") do
          Ch15Cap.say(["(A plain small stone cut with two letters: M.V. An old woman in a sea-coat kneels at it, laying kelp-flowers.)",
                       "Edda: Sprog. I took you out on the night ferry. Brought you back on the last one. Tide's got a sense of humour.",
                       "Edda: She paid me in her Warden's ring. Hers. Off her own hand. I never sold it.",
                       "Edda: Her boy should have it. You give it to him. When you think he'll not throw it in the sea."])
          pbMEPlay("Key item get") rescue nil
          pbMessage("\\me[Key item get]You obtained Morwen's Ring!") rescue nil
        end
      end

      if segs.include?("F")
        Ch15Cap.goto(925, 20, 20, Tone.new(-60, -70, -30, 120), "Convoy marker")
        Ch15Cap.scene("ch15_F_depths") do
          Ch15Cap.say(["(A barrow-door that opens downward. Below your feet: sky, grey and upside-down, going down forever.)",
                       "(A shape like a shadow with a crown of ribs drags itself through a tear in the air. Along its side, a long grey wound like glass.)"])
        end
        gp = Ch15Cap.party((ENV["CK_GLV"] || 70).to_i)
        DemoRun.battle("ch15_F_giratina", gp, turns: 20) do
          Prismfall::Bosses.wild_battle(:GIRATINA_DEPTHS, :can_lose => true)
        end
        log("giratina result #{(Prismfall::Bosses.last_result || {})[:result].inspect}")
      end

      if segs.include?("G")
        Ch15Cap.goto(925, 20, 20, Tone.new(-80, -80, -60, 255), "Convoy marker")
        Ch15Cap.scene("ch15_G_hush") do
          pbBGMStop rescue nil; pbBGSStop rescue nil
          Ch15Cap.wait(60)
          Ch15Cap.say(["(The Hush. No sound at all. Your footsteps show as ripples.)",
                       "(At the far edge the sound comes back: wind, then a bird, then far off, hammers. A lot of hammers. Cogsworth.)",
                       "(In your pocket, Morwen's Ring is cold. Under your collar, the scar is warm.)"])
        end
      end
      log("done")
    end
  end
end
