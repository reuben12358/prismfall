#===============================================================================
# Ch8 Caldera Crisis (map 255) in the real engine, dev tool. Plays the autorun end to end:
# the Hammer double, the detonator, the :ch8_caldera choice and its battle; every battle is
# auto-won after a few frames, choices come from TAP_CHOICES (comma list, 0-based).
#   DEMO_PLAN=tap TAP_CHOICES=1,0   -> throw the detonator away, then vent
# Writes RESULT lines to demo.log: the choice made, V110, S120, CH8_STEP (5 -> 6), where the player ends up and
# whether the crisis actors are gone. TAP_LOSE=1 loses the first Hammer battle instead (the whiteout must leave
# CH8_STEP at 5 and the crisis replayable: no softlock). No frames are recorded unless TAP_SHOTS=1 (every 30th;
# 0.8 MB each and kept twice by run_intro: delete frames/tap_* and captures_keep/tap_* after looking).
#===============================================================================
if ENV["DEMO_PLAN"].to_s.start_with?("tap")
  module TapCap
    @choices = (ENV["TAP_CHOICES"] || "1,0").split(",").map(&:to_i)
    @battles = []
    class << self; attr_accessor :choices, :battles; end
  end
  class << DemoRun
    def run
      self.started = true
      File.write("#{DemoRun::ROOT}/demo.log", "") rescue Dir.mkdir(DemoRun::ROOT)
      log("tap capture boot ok")
      Graphics.transition(0)
      PrismfallMaps.define_singleton_method(:apply_start_position) { false } if defined?(PrismfallMaps)
      Game.start_new
      pbChangePlayer(1)
      $player.name = "Wren"
      $PokemonSystem.textspeed = 2
      $PokemonSystem.battlescene = 1
      $player.party = [DemoRun.mon(:SWAMPERT, 45, [:SURF, :EARTHQUAKE, :ICEBEAM, :PROTECT]),
                       DemoRun.mon(:GARDEVOIR, 45, [:PSYCHIC, :MOONBLAST, :THUNDERBOLT, :PROTECT])]
      $game_variables[129] = 5
      $game_map.setup(255)
      $game_player.moveto(13, 17); $game_player.turn_up
      $scene.disposeSpritesets rescue nil
      $scene.createSpritesets
      $game_map.need_refresh = true
      self.every = 30
      record("tap_#{ENV['TAP_CHOICES'] || '1,0'}".tr(",", "_")) if ENV["TAP_SHOTS"] == "1"
      self.auto = true
      frames = 0
      loop do
        Graphics.update; Input.update
        $scene.update
        frames += 1
        break if frames > 9000
        break if $game_switches[120] && !$game_system.map_interpreter.running? && frames > 200 && $game_screen.tone.red > -100
        break if ENV["TAP_LOSE"] == "1" && TapCap.battles.length > 0 && !$game_system.map_interpreter.running? && !$game_temp.in_battle && frames > 400
      end
      self.auto = false
      stop
      crisis = $game_map.events.values.find { |e| e.name == "The Caldera Crisis" }
      shown = $game_map.events.values.select { |e| e.character_name.to_s != "" && e.opacity > 0 }.map(&:name)
      log("RESULT battles: #{TapCap.battles.inspect}")
      log("RESULT ch8_caldera=#{pf_choice(:ch8_caldera).inspect} V110=#{$game_variables[110]} S120=#{$game_switches[120]} V129=#{$game_variables[129]} " \
          "map=#{$game_map.map_id} pos=#{$game_player.x},#{$game_player.y} tone=#{$game_screen.tone.red.round} actors_left=#{shown.inspect} " \
          "crisis_selfA=#{$game_self_switches[[255, crisis&.id, 'A']].inspect} crisis_trigger=#{crisis&.trigger} frames=#{frames}")
      log("done")
    end
  end
  module Input
    class << self
      alias tap_trigger? trigger? unless method_defined?(:tap_trigger?)
      def trigger?(button)
        return DemoRun.frame % 45 == 0 if button == Input::USE && DemoRun.auto
        return tap_trigger?(button)
      end
    end
  end
  # choices: answer from the queue (the message box still shows)
  alias tap_pbShowCommands pbShowCommands unless defined?(tap_pbShowCommands)
  def pbShowCommands(msgwindow, commands = nil, cmdIfCancel = 0, defaultCmd = 0)
    if DemoRun.auto && commands && commands.length > 1
      pick = TapCap.choices.shift || 0
      DemoRun.log("choice #{pick}: #{commands[pick]}")
      20.times { Graphics.update }
      return pick
    end
    return tap_pbShowCommands(msgwindow, commands, cmdIfCancel, defaultCmd)
  end
  public :pbShowCommands   # pbMessage calls Kernel.pbShowCommands, which needs it public
  class Battle
    alias tap_pbCommandPhase pbCommandPhase unless method_defined?(:tap_pbCommandPhase)
    def pbCommandPhase
      if DemoRun.auto
        names = (@opponent || []).map { |t| "#{t.trainer_type}/#{t.name}" }
        DemoRun.log("battle vs #{names.join(' + ')} field=#{field_effect rescue '?'} partner=#{(@player || []).length > 1}")
        TapCap.battles << names
        60.times { @scene.pbUpdate rescue Graphics.update }
        @decision = (ENV["TAP_LOSE"] == "1" && TapCap.battles.length == 1) ? 2 : 1
        return
      end
      tap_pbCommandPhase
    end
  end
end
