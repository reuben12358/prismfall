#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 18 "Once Upon a Time": key events in the real engine.
# A the Lightless Deep and Pecharunt (181, pink)   B the Verge: Celestine (295)   C Gym 17 Celestine (double)
# D the Hymn of Return   E K7 and Morwen's Ring
# DEMO_PLAN=ch18   CK_SEGS=ABCDE
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch18")
  module Ch18Cap
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
      log("ch18 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch18Cap.party(78)
      15.times { |i| $player.badges[i] = true }
      $bag.add(:MEGARING) rescue nil
      segs = (ENV["CK_SEGS"] || "ABCDEFG").upcase
      if segs.include?("A")
        Ch18Cap.goto(181, 20, 20, Tone.new(30, -30, 0, 60), nil)
        Ch18Cap.scene("ch18_A_deep") do
          Ch18Cap.say(["(A cavern of pink crystal, smelling of peaches. People tending peach-shaped growths with watering-cans. All of them smiling.)",
                       "Mother Gutter: Oh, it's you, topsider. Isn't it lovely down here. I come down every night.",
                       "Mother Gutter: I was the first, you know. The first one it asked. It only wanted company."])
        end
        DemoRun.battle("ch18_A_pecharunt", Ch18Cap.party(79), turns: 16) do
          Prismfall::Bosses.wild_battle(:PECHARUNT_DEEP, :can_lose => true)
        end
        log("pecharunt result #{(Prismfall::Bosses.last_result || {})[:result].inspect}")
        Ch18Cap.goto(181, 20, 20, Tone.new(-60, -60, -50, 80), nil)
        Ch18Cap.scene("ch18_A_after") do
          Ch18Cap.say(["(In the dark, people crying, the way you cry when you wake up from a good dream into a bad week.)",
                       "Mother Gutter: ...Three hundred and eleven years. It says so here. I wrote it down every night. I never read it back."])
        end
      end

      if segs.include?("B")
        Ch18Cap.goto(295, 20, 20, Tone.new(-20, -40, 10, 80), "Evergreen prior")
        Ch18Cap.scene("ch18_B_verge") do
          Ch18Cap.say(["Thornguard Captain: By royal order of His Highness Prince Caedmon, the Gloamwood is closed. Turn back.",
                       "(From the dusk behind the checkpoint, a tall woman in moth-wing grey walks through the thorn barrier as if it weren't there.)",
                       "Celestine: Captain. If you stop this child, the forest will remember your name, and it will say it wrong forever.",
                       "Celestine: One rule. In Gloaming, always ask what it costs before you say yes. Always. Even me."])
        end
      end

      if segs.include?("C")
        16.times { |i| $player.badges[i] = true }
        DemoRun.battle("ch18_C_celestine", Ch18Cap.party(80), turns: (ENV["CK_BT"] || 8).to_i) do
          Prismfall.gym_battle(17, can_lose: true, double: true)
        end
      end

      if segs.include?("D")
        Ch18Cap.goto(295, 20, 20, Tone.new(-30, -40, 0, 90), "Evergreen prior")
        Ch18Cap.scene("ch18_D_hymn") do
          Ch18Cap.say(["Celestine: I've been waiting for you for forty years, little colourless thing. Listen.",
                       "Eighteen we borrowed, eighteen we keep / till the wounded land has learned to sleep;",
                       "then one of no color, the eighteen roads walked, / shall carry them home, as the old ones talked —",
                       "not chained, not broken, not bought, not crowned: / given back, as a gift is found.",
                       "Celestine: Valen reads \"one of no color\" as vessel. The Hollow read it as hammer. Meridian reads it as key.",
                       "Celestine: It says walker."])
        end
      end

      if segs.include?("E")
        17.times { |i| $player.badges[i] = true }
        Ch18Cap.goto(295, 20, 20, Tone.new(-40, -50, -10, 90), "Evergreen prior")
        Ch18Cap.scene("ch18_E_k7pre") do
          Ch18Cap.say(["Kestrel: They all want to use you. Valen wants a lock. Voss wants a key. Your Hollow friends want a crowbar.",
                       "Kestrel: Stay out of Crownhaven and let me end it. I'll make him say her name.",
                       "Kestrel: In stories there's a knight and a dragon. I'm the knight. Guess."])
        end
        DemoRun.battle("ch18_E_k7", Ch18Cap.party(80), turns: 7) do
          Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 7, field: :FAIRY_TALE, can_lose: true)
        end
        Ch18Cap.goto(295, 20, 20, Tone.new(-40, -50, -10, 90), "Evergreen prior")
        Ch18Cap.scene("ch18_E_ring") do
          pbMessage("(He's sitting on a root with his back to you.)", ["Give him Morwen's Ring now", "Keep it for now"], 2, nil, 1)
          Ch18Cap.say(["Wren: Edda kept it. Ten years. She said give it to you when you'd not throw it in the sea.",
                       "(He doesn't say thank you. He puts it on. It fits.)",
                       "Kestrel: Don't come. I mean it. ...You're going to come. Fine. Then don't lose before you reach me."])
        end
      end

      log("done")
    end
  end
end
