#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 14 "The Deep Seams", key events in the real engine.
# Cragholm and the Undersands aren't built; scenes are staged on built maps with the chapter's real lines:
#   A  Cragholm and Bastian's account (Brinecut Mine 1F, 544, lamp-dark)
#   B  Gym 13: Bastian, Crystal Cavern, Mega Aerodactyl "Amber"
#   C  the Ring-Day and the badge case (:ch14_telemetry)
#   D  the raid: Marchetti in the Darkglass gallery, Mega Houndoom on :DARK_CRYSTAL
#   E  Groudon under Duneholt's dry well (staged at the Bone-Carters' Camp, 930)
#   F  Hindmoor: "Who'd sponsor a graveyard?"
#   DEMO_PLAN=ch14   CK_SEGS=ABCDEF   CK_EVERY=4
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch14")
  module Ch14Cap
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
      [DemoRun.mon(:SCEPTILE, 63, [:LEAFSTORM, :GIGADRAIN, :DRAGONPULSE, :FOCUSBLAST], :MIRACLESEED),
       DemoRun.mon(:LUXRAY, 63, [:WILDCHARGE, :ICEFANG, :CRUNCH, :VOLTSWITCH], :LIFEORB),
       DemoRun.mon(:LUCARIO, 62, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:GARCHOMP, 63, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:AGGRON, 62, [:IRONHEAD, :HEAVYSLAM, :EARTHQUAKE, :STONEEDGE], :AGGRONITE),
       DemoRun.mon(:VAPOREON, 62, [:SCALD, :ICEBEAM, :WISH, :PROTECT], :LEFTOVERS)]
    end
  end

  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("ch14 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch14Cap.party
      13.times { |i| $player.badges[i] = true }   # cap 67 after Gym 13 (12 made a Lv 66 party disobey)
      segs = (ENV["CK_SEGS"] || "ABCDEF").upcase

      if segs.include?("A")
        Ch14Cap.goto(544, 20, 20, Tone.new(-40, -50, -60, 30), "Depot cart")
        Ch14Cap.scene("ch14_A_account") do
          Ch14Cap.say(["(Cragholm. A canyon wall of lamplit galleries and lift-cages. Hundreds of little lamps, like a city built inside a lantern.)",
                       "Bastian: Ilsa sent you? Course she did. Sit down. No, there. That crate. I'm telling you about the crown.",
                       "Bastian: AF 290. I was carrying the Stone Plate in the procession. I was nearest the Choir loft.",
                       "Bastian: There was brass behind the loft that had no business in a church. And men in white coats with little gold suns on their pockets, watching dials.",
                       "Bastian: When the Crown cracked, the dials jumped. They weren't surprised.",
                       "Bastian: They were pleased.",
                       "Bastian: I never told. I was afraid. I'm still afraid. I'm telling you anyway."])
        end
      end

      if segs.include?("B")
        DemoRun.battle("ch14_B_bastian", Ch14Cap.party, turns: (ENV["CK_BT"] || 8).to_i) do
          Prismfall.gym_battle(13, can_lose: true, double: false)
        end
      end

      if segs.include?("C")
        Ch14Cap.goto(544, 20, 20, Tone.new(-10, -20, -40, 20), "Depot cart")
        Ch14Cap.scene("ch14_C_ring") do
          Ch14Cap.say(["Bastian: Holloway cut this one. Ten years back. He sent it to me in a sock, with a note: 'It sulks.'",
                       "Bastian: Rock's patient. I reckon this has waited long enough. Hold out your hand.",
                       "(He drops the ring into your palm. The colourless chip catches the lamplight... and sings.)"])
          $game_screen.start_flash(Color.new(255, 255, 230, 220), 24) rescue nil
          Ch14Cap.wait(30)
          Ch14Cap.say(["Pip: Grandad. Grandad, it's SINGING.",
                       "Bastian: Is it? Can't hear a thing. Half-deaf, me.",
                       "(Inside the badge case's lining: a sliver of Lattice-glass, wired to a brass button with a sunburst on the back.)",
                       "Larch: Voss isn't watching you. He's tuning you."])
          pbMessage("Larch: Three ways. Choose. It's your case.", ["Smash it", "Feed it lies", "Leave it"], 3, nil, 1)
          Ch14Cap.say(["Larch: It'll keep singing. Flat. A quarter-tone under every Plate. He'll build his whole machine to a wrong note."])
        end
      end

      if segs.include?("D")
        Ch14Cap.goto(544, 20, 20, Tone.new(-90, -90, -70, 60), "Depot cart")
        Ch14Cap.scene("ch14_D_raid_msgs") do
          Ch14Cap.say(["(The lamps in the upper gallery go out, one after another, all the way down.)",
                       "Thistle: I know where a thread will fall. This one falls here.",
                       "Marchetti: You're not under arrest. You're under — no. I'm not saying 'protection' again. Fight me or step aside."])
        end
        $bag.add(:MEGARING) rescue nil
        DemoRun.battle("ch14_D_marchetti", Ch14Cap.party, turns: (ENV["CK_DT"] || 8).to_i) do
          setBattleRule("field", :DARK_CRYSTAL); setBattleRule("canLose")
          TrainerBattle.start(:MERIDIAN_MARCHETTI, "Helene", 1)
        end
      end

      if segs.include?("E")
        Ch14Cap.goto(930, 20, 20, Tone.new(30, 0, -30, 0), "Elder Ossa")
        Ch14Cap.scene("ch14_E_glyphs") do
          Ch14Cap.say(["(Under Duneholt's dry well: a round hall of red stone cut with Unown glyphs, warm as an oven. In the middle, a hump of red rock rises and falls. It's breathing.)",
                       "Sahar: \"The Year of Two Weathers.\" It's here. It's been here the whole time, under the well, and I dug everywhere else."])
        end
        gparty = Ch14Cap.party
        gparty.each { |p| p.level = (ENV["CK_GLV"] || 66).to_i; p.calc_stats }
        DemoRun.battle("ch14_E_groudon", gparty, turns: 18) do
          Prismfall::Bosses.wild_battle(:GROUDON_UNDERSANDS, :can_lose => true)
        end
        log("groudon result #{(Prismfall::Bosses.last_result || {})[:result].inspect}")
        Ch14Cap.goto(930, 20, 20, Tone.new(10, 0, -10, 0), "Elder Ossa")
        Ch14Cap.scene("ch14_E_well") do
          Ch14Cap.say(["(Silence. Then, very far off, a sound you haven't heard in Duneholt: water.)",
                       "(A child drops a pebble down the well. Everyone listens. A long way down: plink.)",
                       "Sahar: The King woke the red one and the blue one. The sand remembers the sea. It doesn't want it back."])
        end
      end

      if segs.include?("F")
        Ch14Cap.goto(930, 20, 20, Tone.new(-30, -30, -20, 50), "Elder Ossa")
        Ch14Cap.scene("ch14_F_ship") do
          Ch14Cap.say(["(Hindmoor. A shadow goes over you. An airship in Meridian white, a gold sunburst on the envelope, heading north into the fog.)",
                       "(On its side: FELLOWSHIP CHAMPION SERIES — PROUDLY SPONSORING KESTREL VANE.)",
                       "Pip: That's a sponsor ship.",
                       "Pip: Who'd sponsor a graveyard?"])
        end
      end
      log("done")
    end
  end
end
