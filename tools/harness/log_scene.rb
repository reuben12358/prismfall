#===============================================================================
# Logging battle scene + battle runner.
# Harness::LogScene stands in for Battle::Scene (it extends the engine's own
# Battle::DebugSceneNoVisuals) and records every message, HP change, send-out,
# faint, ability splash and field change as plain text.
#===============================================================================
module Harness
  TURN_LIMIT = 150

  class BattleLog
    attr_reader :lines, :errors, :field_changes, :title
    attr_accessor :outcome, :turns, :battle

    def initialize(title)
      @title = title; @lines = []; @errors = []; @field_changes = []; @turn = 0
    end

    def add(text, indent = "  "); @lines << "#{indent}#{text}"; end
    def header(text); @lines << "" << "--- #{text} ---"; end
    def text; ([@title, "=" * @title.length] + @lines).join("\n") + "\n"; end
    def include?(pattern); !find(pattern).nil?; end

    def find(pattern)
      @lines.find { |l| pattern.is_a?(Regexp) ? l =~ pattern : l.include?(pattern) }
    end

    def error(e, where)
      @errors << { :class => e.class.name, :message => e.message, :where => where,
                   :backtrace => (e.backtrace || []).first(14) }
      add("!! EXCEPTION (#{where}) #{e.class}: #{e.message}", "")
      (e.backtrace || []).first(8).each { |b| add("     #{b}", "") }
    end
  end

  class << self
    attr_accessor :current_log
    def log; @current_log; end
  end

  def self.clean(msg)
    s = msg.to_s.dup
    s.gsub!(/\\(wtnp|wt|se|me|ts|c|f|ff|b|r|w|op|cl|g|l)\[[^\]]*\]/i, "")
    s.gsub!(/\\[lnrp1!.|^]/, " ")
    s.gsub!(/<\/?[a-z0-9]+(=[^>]*)?>/i, "")
    s.gsub!(/\s+/, " ")
    s.strip
  end

  def self.who(battler)
    side = battler.opposes? ? "foe" : "player"
    "#{battler.name} (#{side})"
  end

  class LogScene < Battle::DebugSceneNoVisuals
    def initialize(log)
      super(false)
      @log = log
    end

    def pbStartBattle(battle)
      super
      @log.battle = battle
      @log.header("Battle start")
      f = battle.respond_to?(:field_effect) ? battle.field_effect : :NONE
      @log.add("field: #{f}#{(f != :NONE && battle.field_stage != 1) ? " (stage #{battle.field_stage})" : ""}" \
               " | weather: #{battle.field.weather} | terrain: #{battle.field.terrain}")
    end

    def pbBeginCommandPhase
      if @battle.turnCount >= Harness::TURN_LIMIT
        @log.add("** harness turn limit (#{Harness::TURN_LIMIT}) reached: battle stopped as a draw **", "")
        @battle.decision = 5
        return
      end
      @log.header("Turn #{@battle.turnCount + 1}")
      st = @battle.allBattlers.map { |b| "#{b.name} #{b.hp}/#{b.totalhp}#{b.status != :NONE ? " #{b.status}" : ""}" }
      @log.add("[#{st.join(' | ')}]")
    end

    def pbBeginEndOfRoundPhase; @log.add("(end of round)"); end

    def pbDisplayMessage(msg, _brief = false); @log.add(Harness.clean(msg)); end
    alias pbDisplay pbDisplayMessage
    def pbDisplayPausedMessage(msg); @log.add(Harness.clean(msg)); end
    def pbDisplayConfirmMessage(msg)
      # Same answers as the engine's own no-visuals scene (Yes), except the Switch-style prompt.
      yes = !msg.to_s.include?("Will you switch")
      @log.add("#{Harness.clean(msg)}  [auto: #{yes ? 'Yes' : 'No'}]")
      yes
    end
    def pbShowCommands(msg, commands, default); @log.add("#{Harness.clean(msg)} [auto: #{commands[0]}]"); 0; end

    def pbHPChanged(battler, old_hp, _anim = false)
      return if battler.hp == old_hp
      @log.add("  HP #{Harness.who(battler)}: #{old_hp} -> #{battler.hp} / #{battler.totalhp}")
    end

    def pbSendOutBattlers(send_outs, _start = false)
      send_outs.each do |idx, pkmn|
        side = @battle.opposes?(idx) ? "foe" : "player"
        @log.add("  >> sent out (#{side}): #{pkmn.name} Lv.#{pkmn.level}" \
                 "#{pkmn.item_id ? " @#{pkmn.item_id}" : ""} [#{pkmn.ability_id}]")
      end
    end

    def pbRecall(idx); @log.add("  << recalled: #{Harness.who(@battle.battlers[idx])}"); end
    def pbFaintBattler(battler); @log.add("  xx fainted: #{Harness.who(battler)}"); end
    def pbShowAbilitySplash(battler, _delay = false, _log = true)
      @log.add("  [ability: #{Harness.who(battler)}'s #{battler.abilityName}]")
    end
    def pbCommonAnimation(name, _user = nil, _target = nil)
      $stderr.puts("EMPTYANIM " + caller.first(6).join(" | ")) if name.to_s.empty? && ENV["PRISM_TRACE"]
      @log.add("  (anim: #{name})") unless name.to_s.empty?
    end

    # Damage from moves arrives here: [[battler, old_hp, effectiveness], ...]
    def pbHitAndHPLossAnimation(targets)
      targets.each do |t|
        next if t[0].hp == t[1]
        @log.add("  HP #{Harness.who(t[0])}: #{t[1]} -> #{t[0].hp} / #{t[0].totalhp}")
      end
    end
    def pbLevelUp(pkmn, *_a); @log.add("  level up: #{pkmn.name} -> #{pkmn.level}"); end
    def pbEndBattle(result); @log.add("battle result code: #{result}"); end
  end

  OUTCOMES = { 0 => "aborted", 1 => "player won", 2 => "player lost", 3 => "fled/forfeit",
               4 => "caught", 5 => "draw" }.freeze

  # Runs block (which must start a battle through the real overworld API) with
  # a LogScene and AI control of the player's side. Returns the BattleLog.
  def self.run_battle(title, seed: 1, setup: nil)
    log = BattleLog.new(title)
    self.current_log = log
    srand(seed)
    @setup = setup
    begin
      ret = yield
      log.outcome = ret.is_a?(Integer) ? ret : $game_variables[1]
    rescue Exception => e   # recorded, never hidden: reported as a failed battle
      raise if e.is_a?(SystemExit) || e.is_a?(Interrupt)
      log.error(e, "battle")
      log.outcome = nil
      $game_temp.clear_battle_rules
      $game_temp.in_battle = false
    end
    log.turns = log.battle ? log.battle.turnCount : 0
    log.add("")
    log.add("RESULT: #{OUTCOMES[log.outcome] || 'CRASHED'} after #{log.turns} turn(s)", "")
    self.current_log = nil
    @setup = nil
    log
  end

  def self.pending_setup; @setup; end
end

# The scene every battle gets while the harness runs.
module BattleCreationHelperMethods
  module_function
  def create_battle_scene
    return Harness::LogScene.new(Harness.log || Harness::BattleLog.new("unlogged"))
  end
end

# AI plays the player's side; scripted probes may hook in after prepare_battle.
module BattleCreationHelperMethods
  class << self
    alias __harness__prepare_battle prepare_battle unless method_defined?(:__harness__prepare_battle)
    def prepare_battle(battle)
      __harness__prepare_battle(battle)
      battle.controlPlayer = true
      Harness.pending_setup&.call(battle)
    end
  end
end

# Engine error popups (PBDebug.logonerr -> pbPrintException) become log entries.
def pbPrintException(e)
  if Harness.log
    Harness.log.error(e, "engine error popup")
  else
    $stderr.puts("pbPrintException: #{e.class}: #{e.message}\n  " + (e.backtrace || []).first(10).join("\n  "))
  end
end

EventHandlers.add(:prismfall_field_changed, :harness_log,
  proc { |battle, old_id, new_id|
    next if !Harness.log
    stage = battle.respond_to?(:field_stage) ? battle.field_stage : 1
    Harness.log.field_changes << [old_id, new_id, stage]
    if old_id == new_id
      Harness.log.add("## FIELD STAGE: #{new_id} is now stage #{stage}", "")
    else
      Harness.log.add("## FIELD CHANGE: #{old_id} -> #{new_id}", "")
    end
  }
)
