#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 12 "Dead Letters", key events in the real engine.
# Skyreach isn't built, so the scenes are staged on built maps with the chapter's real lines:
# Lumen's Concourse at night (180) for Stormwatch, the Spire's Gala Hall (186) for Voss's office.
#   A  the Larch Papers broadcast and the bomb          B  Gym 11: Odessa, double, Stormfront
#   C  the raid: Marchetti, Mega Manectric (Stormfront) D  K5: Kestrel in the dead-letter archive
#   E  Morwen's letter and :ch12_letter                 F  Interlude III: Voss's office, the drawer
#   DEMO_PLAN=ch12   CK_SEGS=ABCDEF   CK_EVERY=4
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch12")
  module Ch12Cap
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
      [DemoRun.mon(:LUXRAY, 55, [:WILDCHARGE, :ICEFANG, :CRUNCH, :VOLTSWITCH], :LIFEORB),
       DemoRun.mon(:SCEPTILE, 55, [:LEAFSTORM, :GIGADRAIN, :DRAGONPULSE, :FOCUSBLAST], :MIRACLESEED),
       DemoRun.mon(:LUCARIO, 55, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:GARCHOMP, 55, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:MAMOSWINE, 54, [:ICICLECRASH, :EARTHQUAKE, :ICESHARD, :ROCKSLIDE], :NEVERMELTICE),
       DemoRun.mon(:GARDEVOIR, 54, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :CALMMIND], :LEFTOVERS)]
    end
  end

  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch12 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch12Cap.party
      11.times { |i| $player.badges[i] = true }
      night = Tone.new(-90, -80, -20, 50)
      Ch12Cap.goto(180, 48, 40, night, "Meridian Spire")
      segs = (ENV["CK_SEGS"] || "ABCDEF").upcase

      if segs.include?("A")
        Ch12Cap.scene("ch12_A_broadcast") do
          Ch12Cap.say([
            "Odessa: Every Center. Every mast. Every screen in Velmora. You're live in three. Two.",
            "\\pf[LARCH,neutral]Larch: Good evening. My name is Imelda Larch. Every one of you has a light on because of me.",
            "\\pf[LARCH,neutral]Larch: Page four. Lattice extraction accelerates the Bleed. I gave them the rate. I gave them the cities that would go first.",
            "\\pf[LARCH,sad]Larch: Ebbmouth's river. Lumen's Plate. Cindervault's caldera. Rimeholt's lake. In that order. In my handwriting.",
            "\\pf[LARCH,neutral]Larch: I designed the Lattice. I was wrong. I'm telling you now because nobody else will.",
            "\\pf[LARCH,neutral]Larch: Section two. The Unimprinted. In AF 290, at Crownhaven, during the—"])
          $game_screen.start_flash(Color.new(255, 255, 255, 255), 20) rescue nil
          $game_screen.start_shake(8, 9, 40) rescue nil
          pbSEPlay("Battle damage weak") rescue nil
          Ch12Cap.wait(50)
          Ch12Cap.say(["(The relay mast below the booth bends like a reed. The north dishes go up in white light.)",
                       "SIGNAL LOST",
                       "Odessa: Up. UP. That wasn't the storm."])
        end
      end

      if segs.include?("B")
        $game_screen.start_tone_change(Tone.new(0, 0, 0, 0), 0) rescue nil
        Ch12Cap.scene("ch12_B_odessa_msgs") do
          Ch12Cap.say(["Odessa: Hold onto something. No, really.",
                       "Odessa: I carry letters. I don't read them. I don't hand them to a clerk because he said please."])
        end
        DemoRun.battle("ch12_B_odessa", Ch12Cap.party, turns: 4) do
          setBattleRule("canLose")
          Prismfall.gym_battle(11, can_lose: true, double: true)
        end
      end

      if segs.include?("C")
        $game_screen.start_tone_change(night, 0) rescue nil
        Ch12Cap.scene("ch12_C_raid_msgs") do
          Ch12Cap.say(["Marchetti: Nobody is under arrest. You're all under protection.",
                       "\\pf[LARCH,angry]Larch: A Hollow— You did that. Your people did that.",
                       "Marchetti: You're not under arrest. You're under protection. Learn the difference before it's taught to you."])
        end
        DemoRun.battle("ch12_C_marchetti", Ch12Cap.party, turns: (ENV["CK_CT"] || 5).to_i) do
          setBattleRule("field", :STORMFRONT); setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene")
        end
      end

      if segs.include?("D")
        Ch12Cap.scene("ch12_D_k5_msgs") do
          Ch12Cap.say(["(By the hole marked ABROAD, a boy in a new cream-and-gold jacket. On his left hand, a gauntlet of steel and cloudy glass that hums.)",
                       "\\pf[KESTREL,neutral]Kestrel: It's hers. It's the only thing of hers left in the world that isn't a lie somebody else told.",
                       "\\pf[KESTREL,angry]Kestrel: He's going to give me the file. All of it. AF 290. Want to see what this does?"])
        end
        DemoRun.battle("ch12_D_k5", Ch12Cap.party, turns: 5) do
          Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 5, field: :STORMFRONT, can_lose: true)
        end
      end

      if segs.include?("E")
        Ch12Cap.scene("ch12_E_letter") do
          Ch12Cap.say(["(One letter slips out of the bundle and comes down slowly through the dust, at your feet.)",
                       "\"I. — You must not let the child come back. Not for my sake, not for anything.",
                       "If Valen learns what lodged in that little chest, he will put a crown on it.\"",
                       "\"Keep wilting, love. Keep them small and safe and far. I'll carry the name. — M.\""])
          pbMessage("(The letter.)", ["Keep it", "Send it to Kestrel", "Burn it"], 1, nil, 1)
          Ch12Cap.say(["Pip: Kestrel Vane, Meridian Spire, Lumen. It's been undeliverable for twelve years. Not any more."])
        end
      end

      if segs.include?("F")
        Ch12Cap.goto(186, 14, 12, Tone.new(-60, -60, -10, 30), "Voss")
        Ch12Cap.scene("ch12_F_interlude") do
          Ch12Cap.say(["INTERLUDE III — \"Dead Letters\"",
                       "Voss: Kestrel. Come in. Sit. Tea first. You took milk when you were nine. I remember.",
                       "Voss: Your mother was destroyed by a man who thinks he's holding up the sky. I'd like to help you take the sky off him.",
                       "Voss: I have to take a call. Five minutes. Read it properly. I'd hate you to think I'd hidden anything.",
                       "(Calla glances, once, at the left side of the desk. Then at Kestrel.)"])
          pbMessage("(The contract. The drawer.)", ["Sign the contract", "Open the left-hand drawer"], 1, nil, 0)
          Ch12Cap.say(["\\pf[KESTREL,neutral]Kestrel: I'm going to make him say it. In front of everyone. Her name."])
        end
      end
      log("done")
    end
  end
end
