#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 17 "The Drowned Crown": key events in the real engine.
# Underveil and Aurelia aren't built. The scenes are staged on built maps with the chapter's real lines:
#   A Underveil and independence (181)   B Gym 16 Nyx (double)   C the Sun Court: the cradle (295, sea tint)
#   D Voss and Kroll   E Ysolde and Brann   F the docks: END OF ACT IV
#   DEMO_PLAN=ch17   CK_SEGS=ABCDEF   CK_EVERY=4
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch17")
  module Ch17Cap
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
      log("ch17 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch17Cap.party(74)
      15.times { |i| $player.badges[i] = true }
      $bag.add(:MEGARING) rescue nil
      segs = (ENV["CK_SEGS"] || "ABCDEF").upcase
      sea = Tone.new(-60, -10, 0, 60)

      if segs.include?("A")
        Ch17Cap.goto(181, 20, 20, Tone.new(-50, -55, -60, 90), nil)
        Ch17Cap.scene("ch17_A_underveil") do
          Ch17Cap.say(["(Underveil, the morning after the Purge. Smoke. Broken lanterns. Bodies under sheets along the Tier wall.)",
                       "Mother Gutter: Topsider! You're the ferry one. Good. Get up here. We've got a line coming and I've got one Muk.",
                       "Nyx: I've been carrying bodies since midnight. Forty-one.",
                       "Nyx: Underveil isn't on the Accord's maps, sweetheart. That's the point of Underveil. Apparently it's also why nobody comes when they shoot us.",
                       "Nyx: From this hour, Nadir is no part of Zenith. It means nothing. No crown will recognise it.",
                       "Nyx: Say it anyway.",
                       "(The cavern says it back. It's the loudest sound you've ever heard.)"])
        end
      end

      if segs.include?("B")
        DemoRun.battle("ch17_B_nyx", Ch17Cap.party(74), turns: (ENV["CK_BT"] || 8).to_i) do
          Prismfall.gym_battle(16, can_lose: true, double: true)
        end
      end

      if segs.include?("C")
        Ch17Cap.goto(295, 20, 20, sea, "Evergreen prior")
        Ch17Cap.scene("ch17_C_suncourt") do
          Ch17Cap.say(["Sahar: Three hundred years. I've waited my whole life. And don't touch anything gold. Anything.",
                       "(The Sun Court. Gold from floor to dome. Murals: the Blight, the Two Weathers, the Chain, the Calling, the god breaking itself.)",
                       "(A girl in a torn crown pulls a splinter of no colour at all from the wreck of a golden hand: Princess Maren.)",
                       "(In the middle of the throne room: the golden hand itself. The keystone cradle. Its fingers broken at the tips.)"])
          cols = [[255,80,80],[255,160,60],[255,230,80],[120,220,90],[80,200,220],[90,120,255],[180,90,255],[255,120,200],[255,255,255]]
          cols.each { |c| Ch17Cap.flash(Color.new(c[0], c[1], c[2], 150), 8) }
          Ch17Cap.say(["(Your chest is glowing through your shirt. The Sun Court is lit in eighteen colours.)",
                       "Nyx: Oh. Oh, darling. You're the missing piece.",
                       "Sahar: \"Here rests the One that is every color and none.\"",
                       "Sahar: It's the Legend Plate. The god's heart. You've got a piece of it. In you.",
                       "Wren: ...I know. I think I always knew. I just didn't have the word."])
        end
      end

      if segs.include?("D")
        Ch17Cap.goto(295, 20, 20, Tone.new(-40, -10, 10, 60), "Evergreen prior")
        Ch17Cap.scene("ch17_D_voss") do
          Ch17Cap.flash(Color.new(255, 255, 255, 220), 12)
          Ch17Cap.say(["(A cutting-torch through the far wall. A Meridian salvage crew, and among them, helmet under his arm: Aurelian Voss.)",
                       "Voss: House Aurel. My family. We changed the name and kept the grudge.",
                       "Voss: AF 290. My array. My dials. I was very sorry about the forty people. I was even sorrier when I understood what I'd learned.",
                       "Voss: The Lowlight? Twelve people. I made those twelve mean something.",
                       "Voss: Gods are absentee landlords. I'm trying to make sure we never need one again.",
                       "Voss: Your mother wilted in exile because of a broken god. I can fix the god."])
          pbMessage("Voss: Stand with me at the Festival.", ["Refuse", "Feign agreement", "Accept"], 1, nil, 1)
          Ch17Cap.say(["Voss: Of course. You've only known for five minutes. I've known for twenty-five years."])
        end
        DemoRun.battle("ch17_D_kroll", Ch17Cap.party(74), turns: 7) do
          setBattleRule("field", :CAVE); setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_KROLL, "Sabine", 1)
        end
      end

      if segs.include?("E")
        Ch17Cap.goto(181, 20, 20, Tone.new(-40, -45, -50, 80), nil)
        Ch17Cap.scene("ch17_E_brann") do
          Ch17Cap.say(["(The Moon Market steps at dusk. A lantern on every step. Ysolde lights the last one.)",
                       "Ysolde: Is he eating? Kestrel. You'd know better than I would.",
                       "(The Sump Docks. Brann Holloway on a bollard, waiting.)",
                       "Brann: The Tuning is real. It kills Sovereigns. After the Fracture I reset the Crown's stone. I knew it was short.",
                       "Brann: I never asked where the rest went. I don't have to ask now.",
                       "Brann: Valen's arm is crystal to the shoulder. He has weeks. Maybe the Festival.",
                       "Brann: \"Win your last two badges. Then come to me, and I'll tell you everything.\""])
        end
      end

      if segs.include?("F")
        Ch17Cap.goto(181, 20, 20, Tone.new(-70, -70, -50, 100), nil)
        Ch17Cap.scene("ch17_F_docks") do
          Ch17Cap.say(["Nyx: Meridian wants you in that arena. The Accord wants you in that arena. The Hollow wants you in that arena.",
                       "Nyx: Two kings want you as their champion in that arena.",
                       "Nyx: Thirty days, sweetheart. Every power in Velmora is waiting for you to walk into one room.",
                       "Edda: Then we'd best make sure you walk in on your own feet."])
          Ch17Cap.tone(Tone.new(-255, -255, -255, 0), 20)
          Ch17Cap.say(["END OF ACT IV.", "V — SOVEREIGN"])
        end
      end
      log("done")
    end
  end
end
