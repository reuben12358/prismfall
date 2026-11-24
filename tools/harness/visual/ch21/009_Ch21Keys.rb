#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 21 "Sovereign": key events in the real engine.
# A dawn and the Final (Valen)   B the Coronation and the Hijack   C Voss   D Arceus descends, the True Finale
# E Valen into light, Arceus speaks, Homecoming
# DEMO_PLAN=ch21   CK_SEGS=ABCDE
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch21")
  module Ch21Cap
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
      log("ch21 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch21Cap.party(96)
      18.times { |i| $player.badges[i] = true }
      $bag.add(:MEGARING) rescue nil
      segs = (ENV["CK_SEGS"] || "ABCDEFG").upcase
      if segs.include?("A")
        18.times { |i| $player.badges[i] = true }
        Ch21Cap.goto(295, 20, 20, Tone.new(20, 10, -10, 0), "Evergreen prior")
        Ch21Cap.scene("ch21_A_dawn") do
          Ch21Cap.say(["Larch: Don't let him make you a part. He's very good at parts.",
                       "Larch: And win. I've never seen anyone I love win anything.",
                       "Valen: Come on, then. Show me there's another door."])
        end
        DemoRun.battle("ch21_A_final", Ch21Cap.party(96), turns: 8) do
          setBattleRule("field", :PRISM_ARENA); setBattleRule("canLose")
          TrainerBattle.start(:CHAMPION_VALEN, "Valen")
        end
      end

      if segs.include?("B")
        Ch21Cap.goto(295, 20, 20, Tone.new(20, 10, -30, 0), "Evergreen prior")
        Ch21Cap.scene("ch21_B_hijack") do
          Ch21Cap.say(["Valen: Velmora has a new champion.",
                       "(He raises the Crown over your head. The eighteen Plates in the Ring scream.)"])
          Ch21Cap.flash(Color.new(255, 210, 80, 255), 30)
          Ch21Cap.tone(Tone.new(60, 30, -60, 0), 20)
          Ch21Cap.say(["(The arena wakes. Its rings blaze gold. Out of the floor rises a golden hand: the cradle from Aurelia.)",
                       "(The Ring's pylons sprout golden locks. Eighteen. The Gilded Chain.)",
                       "Voss: You carried my key through eighteen doors. Let me show you what it opens.",
                       "Rook: First time Lumen's been dark in ten years. Kinda pretty.",
                       "Magnus: No machine I have built will kill a child. Governor's off. Go.",
                       "Marchetti: All units, stand down. Not for this. Never for this.",
                       "Larch: It's miscalibrated! It's reaching for a shard that isn't where it thinks!"])
        end
      end

      if segs.include?("C")
        DemoRun.battle("ch21_C_voss", Ch21Cap.party(100), turns: 8) do
          setBattleRule("field", :PRISM_ARENA); setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_VOSS, "Aurelian")
        end
      end

      if segs.include?("D")
        Ch21Cap.goto(295, 20, 20, Tone.new(-20, -60, 40, 60), "Evergreen prior")
        Ch21Cap.scene("ch21_D_descends") do
          Ch21Cap.say(["Voss: Then I'll hold it."])
          Ch21Cap.tone(Tone.new(255, 255, 255, 0), 30)
          Ch21Cap.tone(Tone.new(-20, -60, 40, 60), 30)
          Ch21Cap.say(["(The sky opens. Something vast and white is dragged down through it, gold chains snapping onto its wheel. It's in agony.)",
                       "Voss: It's — it's beautiful —",
                       "Valen: Go. Free it. I'll hold the door. I've had thirty years of practice."])
        end
        DemoRun.battle("ch21_D_arceus", Ch21Cap.party(100), turns: 14) do
          Prismfall::Bosses.wild_battle(:ARCEUS_FINALE, :can_lose => true)
        end
      end

      if segs.include?("E")
        Ch21Cap.goto(295, 20, 20, Tone.new(30, 30, 30, 0), "Evergreen prior")
        Ch21Cap.scene("ch21_E_final") do
          Ch21Cap.say(["Celestine: \"— not chained, not broken, not bought, not crowned: given back, as a gift is found.\"",
                       "(Forty thousand people singing a song most of them only learned this week.)",
                       "Valen: Wren.",
                       "(Then he's gone. Light, where he was. The Crown falls, empty, onto the arena floor.)"])
          cols = [[255,80,80],[255,160,60],[255,230,80],[120,220,90],[80,200,220],[90,120,255],[180,90,255],[255,120,200],[255,255,255]]
          cols.each { |c| Ch21Cap.flash(Color.new(c[0], c[1], c[2], 160), 8) }
          Ch21Cap.say(["Arceus: Little light. You have carried me far.",
                       "Arceus: I will not take what is not given. I learned that here."])
          pbMessage("(The last thing you'll say.)", ["\"Go home. Take them with you.\"", "\"I'll keep them.\""], 2, nil, 1)
          Ch21Cap.say(["Wren: Go home. Take them with you."])
          Ch21Cap.tone(Tone.new(80, 80, 80, 0), 40)
          Ch21Cap.say(["(Light rains on Crownhaven. Across the realm, the Bleed recedes in one long exhale.)",
                       "(In the Lowlight, Dex blinks, and finishes his wave.)",
                       "ONE YEAR LATER.",
                       "Edda: Don't lean on my rail like that, sprog."])
        end
      end

      log("done")
    end
  end
end
