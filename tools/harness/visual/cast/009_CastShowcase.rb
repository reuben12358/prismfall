#===============================================================================
# DEV-ONLY (capture copy only, never shipped). New cast art in the real engine: for each trainer,
# two dialogue lines with their portrait, then the B2W2 VS intro and the opening of the battle.
#   DEMO_PLAN=cast   CS_LIST="MERIDIAN_VOSS:Aurelian:0:VOSS,CHAMPION_VALEN:Valen:0:VALEN"   CS_TURNS=1
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("cast")
  module CastCap
    LINES = {
      "VOSS"    => ["\\pf[VOSS,happy]Voss: Kestrel. Come in. Sit. Tea first.", "\\pf[VOSS,neutral]Voss: I'd hate you to think I'd hidden anything."],
      "VALEN"   => ["\\pf[VALEN,neutral]Valen: Find the child.", "\\pf[VALEN,sad]Valen: I have held up the sky for eleven years. Put it down, if you can."],
      "MARISOL" => ["\\pf[MARISOL,angry]Marisol: The Ebb runs both ways. Not our sleds. Not our war.", "\\pf[MARISOL,crying]Marisol: He was nineteen. Nineteen."],
      "ROOK"    => ["\\pf[ROOK,smug]Rook: Rotom says hi.", "\\pf[ROOK,neutral]Rook: Every wire in this city talks. I just listen."],
      "SAHAR"   => ["\\pf[SAHAR,neutral]Sahar: The sand remembers every caravan.", "\\pf[SAHAR,smug]Sahar: Let's see what it remembers of you."],
      "MOURNER" => ["\\pf[MOURNER,neutral]Mourner: Everything that grows must be allowed to die.", "\\pf[MOURNER,angry]Mourner: Pull the nails."]
    }
    def self.party
      [DemoRun.mon(:LUCARIO, 70, [:CLOSECOMBAT, :METEORMASH, :EXTREMESPEED, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:GARCHOMP, 70, [:EARTHQUAKE, :DRAGONCLAW, :STONEEDGE, :SWORDSDANCE], :SITRUSBERRY),
       DemoRun.mon(:GARDEVOIR, 70, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :CALMMIND], :LEFTOVERS)]
    end
  end

  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("cast capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1); $player.name = "Wren"
      $PokemonSystem.textspeed = 1; $PokemonSystem.battlescene = 0
      self.every = (ENV["CK_EVERY"] || 3).to_i
      $player.party = CastCap.party
      18.times { |i| $player.badges[i] = true }
      $game_map.setup((ENV["CS_MAP"] || 147).to_i)
      ev = $game_map.events.values.find { |e| e.name == "Saltwife" }
      $game_player.moveto(ev ? ev.x : 20, ev ? ev.y + 2 : 20)
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      20.times { Graphics.update; $scene.miniupdate }
      (ENV["CS_LIST"] || "MERIDIAN_VOSS:Aurelian:0:VOSS").split(",").each do |item|
        tt, name, ver, id = item.split(":")
        record("cast_#{id.downcase}_talk"); self.auto = true
        (CastCap::LINES[id] || []).each { |l| pbMessage(l) rescue log("msg fail #{$!.message}") }
        20.times { Graphics.update; $scene.miniupdate }
        self.auto = false; stop
        DemoRun.battle("cast_#{id.downcase}_battle", CastCap.party, turns: (ENV["CS_TURNS"] || 1).to_i) do
          setBattleRule("canLose")
          TrainerBattle.start(tt.to_sym, name, ver.to_i)
        end
      end
      log("done")
    end
  end
end
