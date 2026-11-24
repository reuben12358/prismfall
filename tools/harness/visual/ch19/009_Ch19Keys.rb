#===============================================================================
# DEV-ONLY (capture copy only, never shipped). Chapter 19 "The Last Gate": key events in the real engine.
# A Wyrmrest gate and "Weighed"   B the oath   C the Glass Dunes and Reshiram (926, built)
# D the truce   E Gym 18 Sigrun and the 18-tone chord   F the Glassfall Scar
# DEMO_PLAN=ch19   CK_SEGS=ABCDEF
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("ch19")
  module Ch19Cap
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
      log("ch19 capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      Prismfall.record_starter(:SCEPTILE) rescue nil
      self.every = (ENV["CK_EVERY"] || 4).to_i
      $player.party = Ch19Cap.party(84)
      17.times { |i| $player.badges[i] = true }
      $bag.add(:MEGARING) rescue nil
      segs = (ENV["CK_SEGS"] || "ABCDEFG").upcase
      if segs.include?("A")
        Ch19Cap.goto(181, 20, 20, Tone.new(20, -10, -30, 40), nil)
        Ch19Cap.scene("ch19_A_gate") do
          Ch19Cap.say(["Gate-guard: Halt. The pass is closed to all things Zenith-tainted. Say true or say nothing.",
                       "Sigrun: Open it. Wyrmrest is the last gate. Dragons don't let anything through they haven't weighed. I do the weighing. Not my father.",
                       "Sigrun: Dragons don't let anything through they haven't weighed.",
                       "(Her Salamence sniffs you, then sits on you.)",
                       "Sigrun: He says you're light. He says \"eat something\". He's never said that about anyone. Neither have I. Eat something."])
        end
      end

      if segs.include?("B")
        Ch19Cap.goto(181, 20, 20, Tone.new(40, -20, -60, 60), nil)
        Ch19Cap.scene("ch19_B_oath") do
          Ch19Cap.say(["Sigrun: He trained me to be his successor. Then he told me I'd never survive the Crown. And I was relieved. Relieved.",
                       "Sigrun: And then he went looking for you. I knew. For two years I knew, and I let it happen, because it meant it wasn't me.",
                       "Sigrun: Here. Say what you intend to do at the Festival. In Ashkaar, the fire is the court."])
          pbMessage("(The brazier burns white. It's waiting.)", ["\"I'm going to give them back.\"", "\"I'm going to keep them safe.\"", "\"I don't know yet.\"", "\"Whatever you want to hear.\""], 4, nil, 1)
          Ch19Cap.say(["Wren: I'm going to give them back."])
          Ch19Cap.flash(Color.new(255, 255, 255, 200), 16)
          Ch19Cap.say(["(The white fire leans towards you, and then up, like a candle when a door opens.)",
                       "Sigrun: ...It heard. Good."])
        end
      end

      if segs.include?("C")
        Ch19Cap.goto(926, 20, 20, Tone.new(0, 0, 0, 0), nil)
        Ch19Cap.scene("ch19_C_dunes") do
          Ch19Cap.say(["(The Glass Dunes between the two hosts. To the west, a flood-sea under a storm, and something blue and enormous swimming it.)",
                       "Sigrun: I'm Ashkaar. I'll stand with my father's riders unless you give me a reason not to. Give me a reason."])
          pbMessage("Stand between, or take a side?", ["Stand between them", "Back Ashkaar", "Back Isenmar"], 3, nil, 1)
          Ch19Cap.say(["Sigrun: ...Between. Then I'll stand between with you. My father can disown me after.",
                       "(The Light Stone cracks white in the Dominar's hand. Reshiram unfolds over the Siege Camp.)"])
        end
        17.times { |i| $player.badges[i] = true }
        DemoRun.battle("ch19_C_reshiram", Ch19Cap.party(85), turns: 18) do
          Prismfall::Bosses.wild_battle(:RESHIRAM_GLASS_DUNES, :can_lose => true)
        end
        log("reshiram result #{(Prismfall::Bosses.last_result || {})[:result].inspect}")
      end

      if segs.include?("D")
        Ch19Cap.goto(926, 20, 20, Tone.new(-10, -10, 10, 60), nil)
        Ch19Cap.scene("ch19_D_truce") do
          Ch19Cap.say(["(Silence on the dunes. Steam rising off new glass.)",
                       "Sigrun: The legends have left. Reshiram to me. The sea-beast to the sea. Nobody won this morning that the dead would agree with.",
                       "Anja: Settle it at the Festival. By the Boon. Both crowns, one table. I'll count the votes.",
                       "Larch (radio): Look at the mesa. That wasn't a battle to them. That was a reading.",
                       "Sigrun: ...It chose the one who finally said it out loud."])
        end
      end

      if segs.include?("E")
        17.times { |i| $player.badges[i] = true }
        DemoRun.battle("ch19_E_sigrun", Ch19Cap.party(85), turns: (ENV["CK_ET"] || 8).to_i) do
          Prismfall.gym_battle(18, can_lose: true)
        end
        Ch19Cap.goto(181, 20, 20, Tone.new(20, -10, -30, 40), nil)
        Ch19Cap.scene("ch19_E_chord") do
          Ch19Cap.say(["Sigrun: There. There it is. Eighteen."])
          cols = [[255,80,80],[255,160,60],[255,230,80],[120,220,90],[80,200,220],[90,120,255],[180,90,255],[255,120,200],[255,255,255]]
          cols.each { |c| Ch19Cap.flash(Color.new(c[0], c[1], c[2], 160), 8) }
          Ch19Cap.say(["(Your badge case sings. All eighteen tones together, the full chord.)",
                       "Larch (radio): ...He bought it. God help us, he bought it. A quarter-tone flat, all eighteen."])
        end
      end

      if segs.include?("F")
        Ch19Cap.goto(181, 20, 20, Tone.new(-50, -50, -40, 120), nil)
        Ch19Cap.scene("ch19_F_scar") do
          Ch19Cap.say(["(Lower Crownhaven. Standing in the old streets, glass, forty people, exactly where the light caught them.)",
                       "(A Choir cantor with her mouth open mid-note. She isn't Ines. Ines got out.)",
                       "(A little space between two of them where nobody's standing. A child-sized space. You stand in it anyway.)",
                       "(Crownhaven. The new Festival arena, eighteen-sided, gold and glass. Somewhere under the stands, eighteen locks.)"])
        end
      end

      log("done")
    end
  end
end
