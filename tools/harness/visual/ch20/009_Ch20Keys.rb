#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 20 "The Festival of Champions": key events in the real engine.
# A the draw   B the ceremony and the vision   C the Night of Masques   D Valen's audience and Little Owl   E K8 and Morwen's letter
# DEMO_PLAN=ch20   CK_SEGS=ABCDE
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch20")
  module Ch20Cap
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
      log("ch20 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch20Cap.party(94)
      18.times { |i| $player.badges[i] = true }
      $bag.add(:MEGARING) rescue nil
      segs = (ENV["CK_SEGS"] || "ABCDEFG").upcase
      if segs.include?("A")
        Ch20Cap.goto(295, 20, 20, Tone.new(10, 0, -10, 20), "Evergreen prior")
        Ch20Cap.scene("ch20_A_draw") do
          Ch20Cap.say(["(Crownhaven. White stone and bells in a caldera above the clouds. Eighteen banners. The Prism Arena, eighteen-sided, too new.)",
                       "Maelis: Elowen's colours. The forest would be pleased.",
                       "Nyx: Nadir's. We're independent now. It means nothing. Wear it anyway.",
                       "Larch: Or none. There's an old clause. \"The Unsworn.\" Nobody's used it in sixty years."])
          pbMessage("Whose colours?", ["Elowen", "Zenith", "Nadir", "The Unsworn"], 4, nil, 4)
        end
      end

      if segs.include?("B")
        Ch20Cap.goto(295, 20, 20, Tone.new(-30, -40, -10, 60), "Evergreen prior")
        Ch20Cap.scene("ch20_B_ceremony") do
          Ch20Cap.say(["(Dusk. Forty thousand people. Down the Sovereign's Stair, eighteen Wardens, each carrying a Plate.)",
                       "(Dorian. Tamsin. Marisol. Rook. Sahar. Corvin. Brann. Kaito. Juno. Anja. Odessa. Ilsa. Bastian. Ysolde. Magnus. Nyx. Celestine. Sigrun.)",
                       "(Valen takes off the grey glove. His arm is glass, to the shoulder. A sound goes through forty thousand people that isn't a word.)"])
          cols = [[255,80,80],[255,160,60],[255,230,80],[120,220,90],[80,200,220],[90,120,255],[180,90,255],[255,120,200],[255,255,255]]
          cols.each { |c| Ch20Cap.flash(Color.new(c[0], c[1], c[2], 160), 8) }
          Ch20Cap.tone(Tone.new(255, 255, 255, 0), 40)
          Ch20Cap.say(["(In the white: a vast shape of light. A wheel. Eighteen places in the wheel, all empty. One eye, opening.)",
                       "???: ...Little light. You have carried me far."])
          Ch20Cap.tone(Tone.new(-30, -40, -10, 60), 30)
        end
      end

      if segs.include?("C")
        Ch20Cap.goto(181, 20, 20, Tone.new(-40, -40, -30, 80), nil)
        Ch20Cap.scene("ch20_C_masques") do
          Ch20Cap.say(["Dorian: Tonight we tell the truth. It's a novelty. Do try to enjoy it.",
                       "Celestine (as Maren): I broke my father's chain and drowned my father's city. Both of those are true. I'd do the first again.",
                       "The Gilded King (actor): If heaven will not kneel, we'll build a chain.",
                       "(Every head in the square turns to the Meridian box. Voss stands. He applauds. Alone. Warmly.)",
                       "Voss: Bravo. They finally cast the king correctly."])
        end
      end

      if segs.include?("D")
        Ch20Cap.goto(181, 20, 20, Tone.new(-20, -30, -50, 120), nil)
        Ch20Cap.scene("ch20_D_audience") do
          Ch20Cap.say(["Valen: Every ten years Velmora endures. You noticed I never said \"thrives\". Nobody ever notices.",
                       "Valen: I chose a country over a woman's name. I'd do it again. I hate that I'd do it again.",
                       "Valen: You'll hold the Plates quiet for a hundred years. You'll be... very lonely. I'm sorry. I have no other door."])
          pbMessage("What do you say?", ["\"There's another door. The Hymn.\"", "\"Then I'll wear it.\"", "\"You don't get to decide that for me.\""], 3, nil, 1)
          Ch20Cap.say(["Wren: There's another door. The Hymn. We give them back.",
                       "Wren: \"Not chained, not broken, not bought, not crowned: given back, as a gift is found.\"",
                       "Valen: ...Maren wrote that. I thought it was a poem.",
                       "Ilsa: You chose a country over a daughter. Fine. Then save the country, Father.",
                       "Valen: ...Little owl."])
        end
      end

      if segs.include?("E")
        18.times { |i| $player.badges[i] = true }
        DemoRun.battle("ch20_E_k8", Ch20Cap.party(94), turns: 8) do
          Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 8, field: :PRISM_ARENA, can_lose: true)
        end
        Ch20Cap.goto(295, 20, 20, Tone.new(-10, -10, 0, 40), "Evergreen prior")
        Ch20Cap.scene("ch20_E_letter") do
          Ch20Cap.say(["(Ysolde walks out onto the arena floor and gives Kestrel a sealed letter. He reads it there, in front of everyone.)",
                       "\"I didn't fail. I chose. There was a child in the light and I was nearest, and I'd have wanted someone to choose you.\"",
                       "\"I love you more than my seat, more than my name, more than my Plate. That's the whole letter. — Mum.\"",
                       "Kestrel: ...Then you take him. Take him for both of us."])
        end
      end

      log("done")
    end
  end
end
